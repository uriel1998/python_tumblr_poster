#!/usr/bin/env python3
"""
Python CLI tool for posting text content to Tumblr with inline images, hashtags, and links.
Supports both command-line arguments and markdown file input.

Requirements:
    pip install pytumblr python-dotenv

Usage:
    python tumblr_post.py --file text.md
    python tumblr_post.py --title "My Title" --description "Content" --image-url "https://example.com/image.jpg" --alt-text "Alt text" --link "https://example.com" --hashtags "tag1,tag2,tag3"

Environment Variables Required:
    TUMBLR_CONSUMER_KEY
    TUMBLR_CONSUMER_SECRET
    TUMBLR_OAUTH_TOKEN
    TUMBLR_OAUTH_TOKEN_SECRET
    TUMBLR_BLOG_NAME
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

# Check if we should suppress non-error output
LOUD = os.getenv("LOUD") == "1"


def print_info(message: str):
    """Print info message only if LOUD is enabled."""
    if LOUD:
        print(message)


def print_error(message: str):
    """Always print error messages."""
    print(message)


try:
    import pytumblr
except ImportError:
    print(
        "[ERROR] pytumblr is not installed. Please run 'pip install pytumblr' or use the setup script."
    )
    sys.exit(1)

try:
    from dotenv import load_dotenv

    # Try to load .env file if it exists
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print_info(f"[info] Loaded environment variables from {env_file}")
except ImportError:
    # dotenv is optional, continue without it
    pass


class TumblrPoster:
    def __init__(self):
        """Initialize Tumblr client with environment variables."""
        self.consumer_key = os.getenv("TUMBLR_CONSUMER_KEY")
        self.consumer_secret = os.getenv("TUMBLR_CONSUMER_SECRET")
        self.oauth_token = os.getenv("TUMBLR_OAUTH_TOKEN")
        self.oauth_token_secret = os.getenv("TUMBLR_OAUTH_TOKEN_SECRET")
        self.blog_name = os.getenv("TUMBLR_BLOG_NAME")

        # Check for missing environment variables
        missing_vars = []
        if not self.consumer_key:
            missing_vars.append("TUMBLR_CONSUMER_KEY")
        if not self.consumer_secret:
            missing_vars.append("TUMBLR_CONSUMER_SECRET")
        if not self.oauth_token:
            missing_vars.append("TUMBLR_OAUTH_TOKEN")
        if not self.oauth_token_secret:
            missing_vars.append("TUMBLR_OAUTH_TOKEN_SECRET")
        if not self.blog_name:
            missing_vars.append("TUMBLR_BLOG_NAME")

        if missing_vars:
            error_msg = f"""
Missing required environment variables: {", ".join(missing_vars)}

Please set these environment variables either:
1. In your shell environment:
   export TUMBLR_CONSUMER_KEY='your_key'
   export TUMBLR_CONSUMER_SECRET='your_secret'
   export TUMBLR_OAUTH_TOKEN='your_token'
   export TUMBLR_OAUTH_TOKEN_SECRET='your_token_secret'
   export TUMBLR_BLOG_NAME='yourblog.tumblr.com'

2. Or create a .env file in this directory with:
   TUMBLR_CONSUMER_KEY=your_key
   TUMBLR_CONSUMER_SECRET=your_secret
   TUMBLR_OAUTH_TOKEN=your_token
   TUMBLR_OAUTH_TOKEN_SECRET=your_token_secret
   TUMBLR_BLOG_NAME=yourblog.tumblr.com

Get your API credentials at: https://www.tumblr.com/oauth/apps
"""
            raise ValueError(error_msg)

        try:
            self.client = pytumblr.TumblrRestClient(
                self.consumer_key,
                self.consumer_secret,
                self.oauth_token,
                self.oauth_token_secret,
            )

            # Test the connection
            info = self.client.info()
            if "user" not in info:
                raise ValueError(
                    "Failed to authenticate with Tumblr API. Please check your credentials."
                )
            print_info(f"[info] Authenticated as: {info['user']['name']}")

        except Exception as e:
            raise ValueError(f"Failed to initialize Tumblr client: {str(e)}")

    def parse_markdown_file(self, file_path: str) -> Dict[str, str]:
        """
        Parse markdown file to extract post components.
        Expected format:
        Line 1: Title
        Line 2: Hashtags (space-separated, with or without #)
        Rest: Body content with markdown formatting
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) < 3:
            raise ValueError(
                "Markdown file must have at least 3 lines: title, hashtags, and content"
            )

        title = lines[0].strip()
        hashtags_line = lines[1].strip()
        body = "".join(lines[2:]).strip()

        # Parse hashtags
        hashtags = self._parse_hashtags(hashtags_line)

        # Extract image info from markdown
        image_info = self._extract_image_info(body)

        # Extract links from markdown
        links = self._extract_links(body)

        return {
            "title": title,
            "description": body,
            "hashtags": hashtags,
            "image_url": image_info.get("url", ""),
            "alt_text": image_info.get("alt", ""),
            "links": links,
        }

    def _parse_hashtags(self, hashtags_line: str) -> List[str]:
        """Parse hashtags from a line, removing # symbols and splitting by spaces."""
        if not hashtags_line:
            return []

        # Split by spaces and remove # prefix if present
        tags = []
        for tag in hashtags_line.split():
            clean_tag = tag.lstrip("#").strip()
            if clean_tag:
                tags.append(clean_tag)

        return tags

    def _extract_image_info(self, body: str) -> Dict[str, str]:
        """Extract image URL and alt text from markdown img tags."""
        # Match markdown image syntax: ![alt text](url) or <img src="url" alt="alt text">
        md_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
        html_pattern = (
            r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*>'
        )
        html_pattern2 = (
            r'<img[^>]+alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']+)["\'][^>]*>'
        )

        # Try markdown format first
        md_match = re.search(md_pattern, body)
        if md_match:
            return {"alt": md_match.group(1), "url": md_match.group(2)}

        # Try HTML format
        html_match = re.search(html_pattern, body)
        if html_match:
            return {"url": html_match.group(1), "alt": html_match.group(2)}

        html_match2 = re.search(html_pattern2, body)
        if html_match2:
            return {"alt": html_match2.group(1), "url": html_match2.group(2)}

        return {"url": "", "alt": ""}

    def _extract_links(self, body: str) -> List[Dict[str, str]]:
        """Extract links from markdown format [text](url)."""
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        matches = re.findall(pattern, body)

        links = []
        for text, url in matches:
            links.append({"text": text, "url": url})

        return links

    def create_post_content(
        self,
        title: str,
        description: str,
        image_url: str = "",
        alt_text: str = "",
        link: str = "",
        hashtags: List[str] = None,
    ) -> str:
        """
        Create formatted post content with inline image and links.
        """
        content_parts = []

        # Add main description
        if description:
            content_parts.append(description)

        # Add image if provided
        if image_url:
            if alt_text:
                # Use HTML img tag for better alt text support
                img_html = f'<img src="{image_url}" alt="{alt_text}">'
            else:
                # Use markdown format
                img_html = f"![Image]({image_url})"
            content_parts.append(img_html)

        # Add main link if provided
        if link:
            if title:
                link_md = f"[{title}]({link})"
            else:
                link_md = f"[Link]({link})"
            content_parts.append(link_md)

        return "\n\n".join(content_parts)

    def post_text(
        self,
        title: str = "",
        description: str = "",
        image_url: str = "",
        alt_text: str = "",
        link: str = "",
        hashtags: List[str] = None,
        from_file: bool = False,
    ) -> Dict:
        """
        Post text content to Tumblr.

        Args:
            title: Post title
            description: Main post content
            image_url: URL of inline image
            alt_text: Alt text for image
            link: Main link URL
            hashtags: List of hashtags

        Returns:
            Response from Tumblr API
        """
        if hashtags is None:
            hashtags = []

        # Create post content
        if from_file:
            # When parsing from file, description already contains everything
            body = description
        else:
            # When using CLI args, build content from individual pieces
            body = self.create_post_content(
                title, description, image_url, alt_text, link, hashtags
            )

        # Prepare post data
        post_data = {"type": "text", "format": "markdown", "body": body}

        # Add title if provided
        if title:
            post_data["title"] = title

        # Add tags if provided
        if hashtags:
            post_data["tags"] = hashtags

        print_info(f"[info] Posting to blog: {self.blog_name}")
        print_info(f"[info] Title: {title}")
        print_info(f"[info] Tags: {', '.join(hashtags) if hashtags else 'None'}")
        print_info(f"[info] Content length: {len(body)} characters")

        try:
            response = self.client.create_text(self.blog_name, **post_data)

            if "id" in response:
                print_info(f"[info] Post created with ID: {response['id']}")
                if "post_url" in response:
                    print_info(f"[info] Post URL: {response['post_url']}")
                return response
            elif "errors" in response:
                error_msgs = []
                for error in response["errors"]:
                    error_msgs.append(f"  {error.get('detail', error)}")
                print_error(f"[ERROR] Failed to create post:")
                for msg in error_msgs:
                    print_error(msg)
                return response
            else:
                print_error(f"[ERROR] Unexpected response: {response}")
                return response

        except Exception as e:
            print_error(f"[ERROR] Exception occurred: {str(e)}")
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Post text content to Tumblr with inline images, hashtags, and links",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Post from markdown file
    python tumblr_post.py --file text.md

    # Post using command line arguments
    python tumblr_post.py --title "My Post" --description "This is content" \\
                         --image-url "https://example.com/image.jpg" \\
                         --alt-text "Image description" \\
                         --link "https://example.com" \\
                         --hashtags "tag1,tag2,tag3"

Environment Variables Required:
    TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET,
    TUMBLR_OAUTH_TOKEN, TUMBLR_OAUTH_TOKEN_SECRET, TUMBLR_BLOG_NAME
        """,
    )

    # File input option
    parser.add_argument(
        "--file", "-f", help="Path to markdown file containing post content"
    )

    # Individual field options
    parser.add_argument("--title", "-t", help="Post title")
    parser.add_argument("--description", "-d", help="Main post content/description")
    parser.add_argument("--image-url", "-i", help="URL of inline image")
    parser.add_argument("--alt-text", "-a", help="Alt text for image")
    parser.add_argument("--link", "-l", help="Main link URL")
    parser.add_argument(
        "--hashtags", "-ht", help="Comma-separated hashtags (without # symbol)"
    )

    # Debug option
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be posted without actually posting",
    )

    args = parser.parse_args()

    # Check if we have input
    if not args.file and not any([args.title, args.description]):
        parser.error("Must provide either --file or at least --title or --description")

    try:
        poster = TumblrPoster()

        if args.file:
            # Parse from markdown file
            print_info(f"[info] Reading from file: {args.file}")
            try:
                post_data = poster.parse_markdown_file(args.file)

                title = post_data["title"]
                description = post_data["description"]
                image_url = post_data["image_url"]
                alt_text = post_data["alt_text"]
                link = post_data["links"][0]["url"] if post_data["links"] else ""
                hashtags = post_data["hashtags"]
                from_file = True

                print_info(f"[info] Successfully parsed file: {args.file}")
            except Exception as e:
                print_error(f"[ERROR] Error parsing file {args.file}: {str(e)}")
                sys.exit(1)
        else:
            # Use command line arguments
            title = args.title or ""
            description = args.description or ""
            image_url = args.image_url or ""
            alt_text = args.alt_text or ""
            link = args.link or ""
            hashtags = args.hashtags.split(",") if args.hashtags else []
            hashtags = [tag.strip().lstrip("#") for tag in hashtags if tag.strip()]
            from_file = False

        if args.dry_run:
            print_info("\n[info] --- DRY RUN - Content that would be posted ---")
            if from_file:
                content = description
            else:
                content = poster.create_post_content(
                    title, description, image_url, alt_text, link, hashtags
                )
            print_info(f"[info] Title: {title}")
            print_info(f"[info] Tags: {', '.join(hashtags)}")
            print_info(f"[info] Content length: {len(content)} characters")
            print_info(f"[info] Content:\n{content}")
            print_info("[info] --- END DRY RUN ---")
            sys.exit(0)

        # Post to Tumblr
        response = poster.post_text(
            title=title,
            description=description,
            image_url=image_url,
            alt_text=alt_text,
            link=link,
            hashtags=hashtags,
            from_file=from_file,
        )

        if "error" in response or "errors" in response:
            sys.exit(1)

        # If we get here, the post was successful
        sys.exit(0)

    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
