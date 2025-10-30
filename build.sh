#!/bin/bash
set -e

echo "🔧 Installing Python dependencies..."
python -m pip install --upgrade pip setuptools wheel

echo "📦 Installing backend requirements..."
cd backend && python -m pip install -r requirements.txt

echo "✅ Build complete!"