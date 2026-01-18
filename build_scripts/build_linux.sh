#!/bin/bash
# Build script for Linux
# This script creates a distributable version of Load Tester

echo "============================================"
echo "Building Load Tester for Linux"
echo "============================================"
echo

# Check if PyInstaller is installed
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Check if ab binary exists
if [ ! -f "vendor/ab/linux/ab" ]; then
    echo
    echo "ERROR: ab binary not found!"
    echo "Please place ab in vendor/ab/linux/"
    echo "See vendor/ab/README.md for instructions."
    echo
    exit 1
fi

# Make ab executable
chmod +x vendor/ab/linux/ab

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Run PyInstaller
echo
echo "Running PyInstaller..."
pyinstaller build.spec

if [ $? -ne 0 ]; then
    echo
    echo "BUILD FAILED!"
    exit 1
fi

echo
echo "============================================"
echo "Build successful!"
echo "Output: dist/LoadTester/"
echo "============================================"
echo
echo "To run the application:"
echo "  ./dist/LoadTester/LoadTester"
echo
