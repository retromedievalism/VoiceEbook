#!/bin/bash
# One-time setup for VoiceEbook on macOS

set -e

echo "🔍 Checking Python version..."
python3 --version

# Check for Python 3.10+
PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
if [ "$PY_MAJOR" -lt 3 ] || [ "$PY_MINOR" -lt 10 ]; then
  echo ""
  echo "⚠️  Python 3.10 or higher is required (you have $(python3 --version))."
  echo ""
  echo "Install it with Homebrew:"
  echo "  brew install python@3.11"
  echo ""
  echo "Then re-run this script with:"
  echo "  python3.11 -m venv venv"
  echo "  source venv/bin/activate"
  echo "  pip install --upgrade pip"
  echo "  pip install numpy"
  echo "  pip install -r requirements.txt"
  exit 1
fi

echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬆️  Upgrading pip..."
pip install --upgrade pip

echo "📥 Installing numpy first (required by other packages)..."
pip install numpy

echo "📥 Installing remaining dependencies (this may take a few minutes)..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the app, run:"
echo "  bash start.sh"
echo ""
echo "Then open http://localhost:5000 in your browser."
