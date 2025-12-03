# Python Tumblr Text Poster

A Python CLI tool for posting text content to Tumblr with inline images, hashtags, and links. This is a refactored version of the original Go implementation with enhanced features and better usability.

## Features

- 🖼️ **Inline Images**: Support for images with alt text for accessibility
- 🏷️ **Hashtags**: Automatic hashtag parsing and formatting
- 🔗 **Links**: Support for markdown-style links
- 📝 **Markdown Support**: Full markdown formatting in posts
- 📄 **File Input**: Read post content from markdown files
- ⌨️ **CLI Arguments**: Direct command-line input for quick posts
- 🧪 **Dry Run**: Preview posts before publishing
- 🐍 **Virtual Environment**: Isolated dependency management

## Prerequisites

- Python 3.6 or higher
- Tumblr API credentials (Consumer Key, Consumer Secret, OAuth Token, OAuth Token Secret)
- A Tumblr blog

## Quick Setup

1. **Clone/Download** this repository
2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. **Set up your Tumblr API credentials** (see [API Setup](#api-setup) below)
4. **Test the installation**:
   ```bash
   ./run_tumblr.sh --dry-run --file example_post.md
   ```

## API Setup

### Getting Tumblr API Credentials

1. Go to [Tumblr API Console](https://www.tumblr.com/oauth/apps)
2. Register a new application
3. Note down your Consumer Key and Consumer Secret
4. Generate OAuth tokens for your blog

### Setting Environment Variables

Add these to your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
export TUMBLR_CONSUMER_KEY='your_consumer_key_here'
export TUMBLR_CONSUMER_SECRET='your_consumer_secret_here'
export TUMBLR_OAUTH_TOKEN='your_oauth_token_here'
export TUMBLR_OAUTH_TOKEN_SECRET='your_oauth_token_secret_here'
export TUMBLR_BLOG_NAME='yourblogname.tumblr.com'
```

Or create a `.env` file in the project directory:

```bash
# Create .env file
cat > .env << 'EOF'
TUMBLR_CONSUMER_KEY=your_consumer_key_here
TUMBLR_CONSUMER_SECRET=your_consumer_secret_here
TUMBLR_OAUTH_TOKEN=your_oauth_token_here
TUMBLR_OAUTH_TOKEN_SECRET=your_oauth_token_secret_here
TUMBLR_BLOG_NAME=yourblogname.tumblr.com
EOF

# Load environment variables
source .env
```

## Usage

### Option 1: Using Markdown Files (Recommended)

Create a markdown file with this format:

```markdown
Your Post Title Here
#hashtag1 #hashtag2 #hashtag3

This is your post content. You can use **markdown formatting** like *italic* and **bold** text.

<img src="https://example.com/image.jpg" alt="Descriptive alt text for accessibility">

You can include [links like this](https://example.com) and multiple paragraphs.

[Another link](https://another-example.com)
```

Then post it:

```bash
# Using the convenience script (recommended)
./run_tumblr.sh --file your_post.md

# Or activate venv manually
source venv/bin/activate
python3 tumblr_post.py --file your_post.md
```

### Option 2: Command Line Arguments

```bash
./run_tumblr.sh \
    --title "My Amazing Post" \
    --description "This is the main content of my post with **markdown** support." \
    --image-url "https://example.com/image.jpg" \
    --alt-text "Description of the image" \
    --link "https://example.com/source" \
    --hashtags "technology,programming,python"
```

### Option 3: Dry Run (Preview Before Posting)

```bash
# Preview what will be posted
./run_tumblr.sh --dry-run --file your_post.md

# Or with CLI arguments
./run_tumblr.sh --dry-run \
    --title "Test Post" \
    --description "Test content" \
    --hashtags "test,preview"
```

## File Format Examples

### Basic Post
```markdown
Simple Blog Post
#blogging #writing

This is a simple blog post with just text content and hashtags.
```

### Post with Image
```markdown
Post with Image
#photography #art

Check out this amazing artwork:

<img src="https://example.com/artwork.jpg" alt="Beautiful digital artwork showing a sunset over mountains">

The image above demonstrates the use of vibrant colors in digital art.
```

### Post with Links
```markdown
Resource Collection
#resources #learning

Here are some great resources for learning:

- [Python Documentation](https://docs.python.org/)
- [Markdown Guide](https://www.markdownguide.org/)

Check out the [main resource hub](https://example.com/resources) for more links.
```

### Complete Example
```markdown
Complete Tutorial: Python Web Scraping
#python #tutorial #webscraping #programming

Learn how to scrape websites responsibly with Python! This comprehensive guide covers everything from basic requests to advanced techniques.

<img src="https://example.com/python-scraping.png" alt="Python code example showing web scraping with Beautiful Soup">

## What you'll learn:
- HTTP requests with the `requests` library
- HTML parsing with Beautiful Soup
- Handling forms and sessions
- Rate limiting and ethics

[Read the full tutorial](https://example.com/python-scraping-tutorial)

Additional resources:
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)
```

## Command Line Options

```
usage: tumblr_post.py [-h] [--file FILE] [--title TITLE] [--description DESCRIPTION] 
                     [--image-url IMAGE_URL] [--alt-text ALT_TEXT] [--link LINK] 
                     [--hashtags HASHTAGS] [--dry-run]

Post text content to Tumblr with inline images, hashtags, and links

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Path to markdown file containing post content
  --title TITLE, -t TITLE
                        Post title
  --description DESCRIPTION, -d DESCRIPTION
                        Main post content/description
  --image-url IMAGE_URL, -i IMAGE_URL
                        URL of inline image
  --alt-text ALT_TEXT, -a ALT_TEXT
                        Alt text for image
  --link LINK, -l LINK  Main link URL
  --hashtags HASHTAGS, -ht HASHTAGS
                        Comma-separated hashtags (without # symbol)
  --dry-run            Show what would be posted without actually posting
```

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Make sure all Tumblr API credentials are set
   - Check that variable names are exactly as specified
   - Restart your terminal after setting environment variables

2. **"Module 'pytumblr' not found"**
   - Run the setup script: `./setup.sh`
   - Or manually activate venv: `source venv/bin/activate`

3. **"Permission denied" when running scripts**
   - Make scripts executable: `chmod +x setup.sh run_tumblr.sh tumblr_post.py`

4. **API authentication errors**
   - Verify your API credentials are correct
   - Check that your OAuth tokens haven't expired
   - Ensure your app has the necessary permissions

### Debug Mode

Add debug prints by modifying the script or use the dry-run option to see exactly what will be posted:

```bash
./run_tumblr.sh --dry-run --file your_post.md
```

## Important Fixes

### Hashtag Processing Fix
This Python version fixes a critical bug where hashtags were being split into individual letters instead of proper tags. The issue was caused by passing hashtags as a comma-separated string instead of a Python list to the Tumblr API.

**Fixed behavior:**
- Input: `#technology #programming #python` 
- Result: Tags are correctly created as "technology", "programming", "python"
- Previously would have created: "t", "e", "c", "h", "n", "o", "l", "o", "g", "y", etc.

## Comparison with Go Version

| Feature | Go Version | Python Version |
|---------|------------|----------------|
| File Input | ✅ text.md | ✅ Any .md file |
| CLI Arguments | ❌ | ✅ Full support |
| Inline Images | ❌ | ✅ With alt text |
| Multiple Links | ❌ | ✅ Auto-detected |
| Hashtag Parsing | ⚠️ JSON format | ✅ Fixed & Enhanced |
| Dry Run | ❌ | ✅ Preview mode |
| Virtual Environment | ❌ | ✅ Isolated deps |
| Error Handling | ✅ Basic | ✅ Comprehensive |

## Contributing

Feel free to submit issues and enhancement requests! The code is designed to be easily extensible for additional Tumblr post types and features.

## License

This project maintains the same license as the original Go implementation.