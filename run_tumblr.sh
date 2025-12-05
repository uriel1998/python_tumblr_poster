#!/bin/bash
# Convenience script to run tumblr_post.py with the virtual environment activated

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

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

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    print_error "[ERROR] Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Check if virtual environment activation script exists
if [ ! -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    print_error "[ERROR] Virtual environment activation script not found. Please run ./setup.sh to recreate."
    exit 1
fi

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Check if activation was successful
if [ $? -ne 0 ]; then
    print_error "[ERROR] Failed to activate virtual environment."
    exit 1
fi

# Run the Python script with all passed arguments and capture its exit code
python3 "$SCRIPT_DIR/tumblr_post.py" "$@"
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

# Exit with the same code as the Python script
exit $EXIT_CODE
