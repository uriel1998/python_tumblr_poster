#!/bin/bash
# Convenience script to run tumblr_post.py with the virtual environment activated

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Run the Python script with all passed arguments
python3 "$SCRIPT_DIR/tumblr_post.py" "$@"
