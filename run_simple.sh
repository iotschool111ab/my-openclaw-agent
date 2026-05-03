#!/bin/bash
# Run the simple LINE BOT server (direct Groq API)

# Load environment variables from .env file
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Check if required variables are set
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ] || [ -z "$LINE_CHANNEL_SECRET" ] || [ -z "$GROQ_API_KEY" ]; then
    echo "❌ Please set LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, and GROQ_API_KEY in .env file"
    exit 1
fi

echo "🚀 Starting simple LINE BOT server with direct Groq API..."
python main_simple.py