import os
import subprocess
import tempfile
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, FileMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# LINE BOT configuration
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# Set Groq API key for OpenClaw
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # Process message with OpenClaw agent
    response = process_with_openclaw(user_message, user_id)

    # Reply to user
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=response)
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_id = event.message.id
    user_id = event.source.user_id

    # Download image
    message_content = line_bot_api.get_message_content(message_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(message_content.content)
        temp_file_path = temp_file.name

    # Process image with OpenClaw agent
    response = process_image_with_openclaw(temp_file_path, user_id)

    # Clean up temp file
    os.unlink(temp_file_path)

    # Reply to user
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=response)
    )

@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_id = event.message.id
    file_name = event.message.file_name
    user_id = event.source.user_id

    # Download file
    message_content = line_bot_api.get_message_content(message_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix='_' + file_name) as temp_file:
        temp_file.write(message_content.content)
        temp_file_path = temp_file.name

    # Process file with OpenClaw agent
    response = process_file_with_openclaw(temp_file_path, file_name, user_id)

    # Clean up temp file
    os.unlink(temp_file_path)

    # Reply to user
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=response)
    )

def process_with_openclaw(message, user_id):
    # Use OpenClaw CLI to process the message with local agent
    try:
        result = subprocess.run(
            ['openclaw', 'agent', '--local', '--message', message, '--json'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            # Parse JSON response
            import json
            response_data = json.loads(result.stdout)
            return response_data.get('reply', 'Message processed successfully')
        else:
            return f"Error processing message: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Processing timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def process_image_with_openclaw(image_path, user_id):
    # For images, describe the image with OpenClaw
    try:
        result = subprocess.run(
            ['openclaw', 'agent', '--local', '--message', f'Please describe this image: {image_path}', '--json'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            import json
            response_data = json.loads(result.stdout)
            return response_data.get('reply', 'Image processed successfully')
        else:
            return f"Error processing image: {result.stderr}"
    except Exception as e:
        return f"Error processing image: {str(e)}"

def process_file_with_openclaw(file_path, file_name, user_id):
    # For files, summarize or process with OpenClaw
    try:
        result = subprocess.run(
            ['openclaw', 'agent', '--local', '--message', f'Please process this file {file_name}: {file_path}', '--json'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            import json
            response_data = json.loads(result.stdout)
            return response_data.get('reply', 'File processed successfully')
        else:
            return f"Error processing file: {result.stderr}"
    except Exception as e:
        return f"Error processing file: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)