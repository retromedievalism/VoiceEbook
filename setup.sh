#!/bin/bash
# One-time setup for VoiceEbook on macOS

set -e

echo "🔍 Checking Python version..."
python3 --version

echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬆️  Upgrading pip..."
pip install --upgrade pip

echo "📥 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the app, run:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open http://localhost:5000 in your browser."
