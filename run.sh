#!/bin/bash
# Run the LINE BOT server

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Check if required variables are set
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ] || [ -z "$LINE_CHANNEL_SECRET" ] || [ -z "$GROQ_API_KEY" ]; then
    echo "❌ Please set LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, and GROQ_API_KEY in .env file"
    exit 1
fi

echo "🚀 Starting LINE BOT server with Groq AI..."
python main.py