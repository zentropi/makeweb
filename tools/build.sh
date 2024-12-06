#!/bin/sh
#
# Build script for MakeWeb.
#

build_lib_manifest() {
    # Create lib manifest file
    echo "Creating lib manifest file..."

    # A little dance to avoid including the manifest file itself.
    rm -f lib/manifest.py
    find lib -name "*.py" | sed 's|^lib/||' | awk '{print "module(\"" $1 "\")"}' >lib_manifest.py
    mv lib_manifest.py lib/manifest.py
}

build_lib_manifest

makeweb_binary_name="makeweb"
manifest_path="$(pwd)/manifest.py"
makeweb_binary_path="$(pwd)/$makeweb_binary_name"

# Build mpy-cross
echo "Building mpy-cross..."
cd upstream/micropython/mpy-cross &&
    make || exit

# Return to project root
cd - >/dev/null || exit

# Build MakeWeb binary
echo "Building MakeWeb binary..."
cd upstream/micropython/ports/unix &&
    make FROZEN_MANIFEST="$manifest_path" CFLAGS_EXTRA="-Wno-error -g" LDFLAGS_EXTRA="-lpthread -ldl" || exit

# Return to project root
cd - >/dev/null || exit

# Copy MakeWeb binary to project root
cp upstream/micropython/ports/unix/build-standard/micropython "$makeweb_binary_path"

# Set MakeWeb binary as executable
chmod +x "$makeweb_binary_path"

echo "MakeWeb binary built successfully at $makeweb_binary_path"
