from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

api_key = os.getenv('PPLX_API_KEY')
client = OpenAI(api_key=api_key, base_url='https://api.perplexity.ai')

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        response = client.chat.completions.create(
            model='sonar-pro',
            messages=[
                {'role': 'system', 'content': 'You are an AI image generation assistant. Describe how to create this image.'},
                {'role': 'user', 'content': f'Generate image: {prompt}'}
            ],
            max_tokens=200
        )
        
        return jsonify({
            'prompt': prompt,
            'description': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'image-bot'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

