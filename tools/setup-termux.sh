#!/bin/sh
#
# Install Termux, Termux:API, Termux:Widget and Termux:Boot
# from f-droid or Google Play Store.
#
# Then run the following commands in Termux:
#
# termux-setup-storage
#
# pkg update
# pkg upgrade
# pkg install openssh
#
# whoami(note the username)
# passwd
# openssh -p 2222
#
# If you have tailscale, us the IP address from "tailscale status",
# otherwise use the IP address from ifconfig.
#
# ssh -p 2222 <username>@<ip_address>
#
#  Now you can run the following commands in Termux via ssh:
#
# git clone https://github.com/zentropi/makeweb.git

# Run this script in Termux to apply the Android-specific patches
# to the MicroPython source code.
#
# Install required packages

pkg install termux-api
pkg install binutils git patch python rsync

# Get the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

# Apply the Android-specific patches
patch "upstream/micropython/ports/unix/mpthreadport.c" "$SCRIPT_DIR/mpthreadport.diff"

# Check if patch was successful
if [ $? -eq 0 ]; then
    echo "Successfully patched mpthreadport.c"
else
    echo "Failed to patch mpthreadport.c"
    exit 1
fi
