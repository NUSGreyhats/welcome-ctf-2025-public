#!/bin/bash

echo "Building flag_enhancer.exe and not_sus.dll..."
echo "============================================="

# Check if MinGW is installed
if ! command -v x86_64-w64-mingw32-gcc &> /dev/null; then
    echo "Error: MinGW-w64 not found. Please install it first:"
    echo "Ubuntu/Debian: sudo apt install mingw-w64"
    echo "Arch: sudo pacman -S mingw-w64-gcc"
    echo "macOS: brew install mingw-w64"
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -f flag_enhancer.exe not_sus.dll *.o *.lib

# Compile the DLL
echo "Building not_sus.dll..."
x86_64-w64-mingw32-gcc -shared -o not_sus.dll not_sus.c -Wl,--out-implib,not_sus.lib

if [ ! -f "not_sus.dll" ]; then
    echo "Error: Failed to build not_sus.dll"
    exit 1
fi

# Compile the main flag enhancer executable
echo "Building flag_enhancer.exe..."
x86_64-w64-mingw32-gcc -o flag_enhancer.exe flag_enhancer.c

if [ ! -f "flag_enhancer.exe" ]; then
    echo "Error: Failed to build flag_enhancer.exe"
    exit 1
fi

# Clean up intermediate files
echo "Cleaning up intermediate files..."
rm -f *.o *.lib

echo ""
echo "Build completed successfully!"
echo "============================"
echo "Built files: flag_enhancer.exe, not_sus.dll"
echo ""
echo "To test:"
echo "1. Run: wine flag_enhancer.exe (or .\\flag_enhancer.exe on Windows)"
echo "2. Check for flag.blackhat file with encrypted flag"
