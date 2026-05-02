#!/bin/bash
echo "Generating Sprint 1, 2, 3 files..."

# This script creates all missing module files
cd /workspace/backend/app/modules

# Create __init__.py for modules
touch student/__init__.py finance/__init__.py attendance/__init__.py

echo "✅ Module directories initialized"
echo "Next: Creating model files..."
