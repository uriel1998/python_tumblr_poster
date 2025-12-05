#!/bin/bash

# Setup script for Tumblr Python posting tool
# This script creates a virtual environment and installs dependencies

set -e  # Exit on error

# Check if we should suppress non-error output
LOUD=${LOUD:-0}

print_info() {
    if [ "$LOUD" = "1" ]; then
        echo "$1"
    fi
}

print_error() {
    echo "$1"
}

print_info "[info] Setting up Tumblr Python posting tool with virtual environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "[ERROR] Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

print_info "[info] Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "[info] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        print_error "[ERROR] Failed to create virtual environment."
        exit 1
    fi
    print_info "[info] Virtual environment created"
else
    print_info "[info] Virtual environment already exists"
fi

# Activate virtual environment
print_info "[info] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "[ERROR] Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip in virtual environment
print_info "[info] Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    print_error "[ERROR] Failed to upgrade pip."
    exit 1
fi

# Install Python dependencies
print_info "[info] Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "[ERROR] Failed to install Python dependencies."
    exit 1
fi

print_info "[info] Dependencies installed successfully!"

print_info ""
print_info "[info] Setup complete!"
print_info ""
print_info "[info] Next steps:"
print_info "1. Set up your Tumblr API credentials as environment variables:"
print_info "   export TUMBLR_CONSUMER_KEY='your_consumer_key'"
print_info "   export TUMBLR_CONSUMER_SECRET='your_consumer_secret'"
print_info "   export TUMBLR_OAUTH_TOKEN='your_oauth_token'"
print_info "   export TUMBLR_OAUTH_TOKEN_SECRET='your_oauth_token_secret'"
print_info "   export TUMBLR_BLOG_NAME='yourblogname.tumblr.com'"
print_info ""
print_info "2. You can add these to your ~/.bashrc or ~/.zshrc to make them permanent"
print_info ""
print_info "3. Test the installation using the convenience script:"
print_info "   ./run_tumblr.sh --dry-run --file example_post.md"
print_info ""
print_info "4. Or activate the virtual environment manually and run directly:"
print_info "   source venv/bin/activate"
print_info "   python3 tumblr_post.py --dry-run --file example_post.md"
print_info ""
print_info "5. Create your first post:"
print_info "   ./run_tumblr.sh --file text.md"
print_info ""
print_info "[info] For more help, run: ./run_tumblr.sh --help"
print_info ""
print_info "[info] The convenience script './run_tumblr.sh' automatically activates the virtual environment"
print_info "   and runs the Python script, so you don't have to remember to activate it each time."

# Exit with success code
exit 0
