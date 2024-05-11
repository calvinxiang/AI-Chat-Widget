from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
import anthropic
import os
from dotenv import load_dotenv
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

load_dotenv()

app = Flask(__name__)
CORS(app)

chroma_client = chromadb.PersistentClient(path="./chroma")


try:
    collection = chroma_client.create_collection("chat_history")
except chromadb.db.base.UniqueConstraintError:
    collection = chroma_client.get_collection("chat_history")


embedding_functions = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

client = anthropic.Anthropic(
    api_key = os.getenv("ANTHROPIC_API_KEY")
)

@app.route('/chat', methods=['POST'])
def handle_chat():
    print("Chat endpoint reached")
    if request.headers.get('Content-Type') == 'application/json':
        print(f"Raw JSON received: {request.json}")
        user_message = request.json['message']

        conversation_history = get_conversation_history()
        conversation_history.append({
            "role": "user",
            "content": f"{user_message}"
        })
        try:
            print(f"Received message: {user_message}")
            message = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1024,
                    messages=conversation_history
            )
            result = message.content[0].text
            print(f"LLM response: {result}")

            # Store chat history in ChromaDB
            new_user_msg_id = f'msg_{len(collection.get())+1}'
            new_assistant_message = f'msg_{len(collection.get())+2}'
            collection.add(
                documents=[user_message, result],
                metadatas=[{"role": "user"}, {"role": "assistant"}],
                ids=[new_user_msg_id, new_assistant_message]
            )
            return jsonify({'response': result})
        except Exception as e:
            print(f"Error in handle_chat: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    else:
        return 'Unsupported Media Type', 415

def get_conversation_history():
    conversation_history = []
    messages = collection.get()
    last_role = None
    for doc, meta in zip(messages['documents'], messages['metadatas']):
        current_role = meta['role']
        if current_role != last_role:
            conversation_history.append({"role": current_role, "content": doc})
            last_role = current_role
    return conversation_history


if __name__ == '__main__':
    app.run()