#!/bin/bash

# Setup script for Tumblr Python posting tool
# This script creates a virtual environment and installs dependencies

set -e  # Exit on error

echo "[info] Setting up Tumblr Python posting tool with virtual environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

echo "[info] Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[info] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment."
        exit 1
    fi
    echo "[info] Virtual environment created"
else
    echo "[info] Virtual environment already exists"
fi

# Activate virtual environment
echo "[info] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip in virtual environment
echo "[info] Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to upgrade pip."
    exit 1
fi

# Install Python dependencies
echo "[info] Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install Python dependencies."
    exit 1
fi

echo "[info] Dependencies installed successfully!"

echo ""
echo "[info] Setup complete!"
echo ""
echo "[info] Next steps:"
echo "1. Set up your Tumblr API credentials as environment variables:"
echo "   export TUMBLR_CONSUMER_KEY='your_consumer_key'"
echo "   export TUMBLR_CONSUMER_SECRET='your_consumer_secret'"
echo "   export TUMBLR_OAUTH_TOKEN='your_oauth_token'"
echo "   export TUMBLR_OAUTH_TOKEN_SECRET='your_oauth_token_secret'"
echo "   export TUMBLR_BLOG_NAME='your_blog_name.tumblr.com'"
echo ""
echo "2. You can add these to your ~/.bashrc or ~/.zshrc to make them permanent"
echo ""
echo "3. Test the installation using the convenience script:"
echo "   ./run_tumblr.sh --dry-run --file example_post.md"
echo ""
echo "4. Or activate the virtual environment manually and run directly:"
echo "   source venv/bin/activate"
echo "   python3 tumblr_post.py --dry-run --file example_post.md"
echo ""
echo "5. Create your first post:"
echo "   ./run_tumblr.sh --file text.md"
echo ""
echo "[info] For more help, run: ./run_tumblr.sh --help"
echo ""
echo "[info] The convenience script './run_tumblr.sh' automatically activates the virtual environment"
echo "   and runs the Python script, so you don't have to remember to activate it each time."

# Exit with success code
exit 0
