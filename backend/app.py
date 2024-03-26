from flask import Flask, request, jsonify
from flask_cors import CORS
# from langchain.llms import LlamaCpp
from transformers import pipeline
import anthropic

app = Flask(__name__)
CORS(app)

# pipe = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")
anthropic_api_key = ''
client = anthropic.Anthropic(
    api_key = anthropic_api_key
)

# llm = LlamaCpp(model_path=r"C:\Users\Calvin\.cache\lm-studio\models\TheBloke\Mistral-7B-Instruct-v0.1-GGUF\mistral-7b-instruct-v0.1.Q2_K.gguf")

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