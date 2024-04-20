from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
import anthropic
import os
from dotenv import load_dotenv
from chromadb.utils import embedding_functions
from chromadb.config import Settings

load_dotenv()

app = Flask(__name__)
CORS(app)

chroma_client = chromadb.Client()

client = anthropic.Anthropic(
    api_key = os.getenv("ANTHROPIC_API_KEY")
)

@app.route('/chat', methods=['POST'])
def handle_chat():
    if request.headers.get('Content-Type') == 'application/json':
        user_message = request.json['message']
        try:
            print(f"Received message: {user_message}")
            message = client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": f"{user_message}"}
                    ]
            )
            result = message.content[0].text
            print(f"LLM response: {result}")
            return jsonify({'response': result})
        except Exception as e:
            print(f"Error in handle_chat: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    else:
        return 'Unsupported Media Type', 415

if __name__ == '__main__':
    app.run()