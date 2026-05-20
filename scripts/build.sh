#!/usr/bin/env bash
# Build script for cmcli

set -e

cd "$(dirname "$0")/.."

echo "📦 Building cmcli..."

# Install in dev mode
pip install -e .

# Verify
cmcli --help
cmcli version

echo "✅ Done"
