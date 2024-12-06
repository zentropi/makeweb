#!/bin/sh
#
# Build clean script for MakeWeb.
#

cd upstream/micropython/ports/unix &&
    gmake clean || exit
