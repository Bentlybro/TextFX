from flask import Flask, request, send_file
from flask_cors import CORS
from generators.gradient_text import generate_gradient_text, generate_animated_gradient_text
from generators.neon_text import generate_neon_text
from generators.rainbow_wave import generate_rainbow_wave
from generators.glitch_text import generate_glitch_text
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return {
        'name': 'TextFX API',
        'version': '1.0.0',
        'endpoints': [
            {
                'path': '/api/v1/gradient-text',
                'description': 'Generate static RGB gradient text on transparent background',
                'method': 'GET',
                'params': {
                    'text': 'Text to display with gradient effect'
                }
            },
            {
                'path': '/api/v1/gradient-text.gif',
                'description': 'Generate animated scrolling RGB gradient text effect (GIF)',
                'method': 'GET',
                'params': {
                    'text': 'Text to display with animated gradient effect'
                }
            },
            {
                'path': '/api/v1/neon',
                'description': 'Generate text with neon glow effect',
                'method': 'GET',
                'params': {
                    'text': 'Text to display with neon effect'
                }
            },
            {
                'path': '/api/v1/rainbow-wave',
                'description': 'Generate text with rainbow wave pattern',
                'method': 'GET',
                'params': {
                    'text': 'Text to display with rainbow wave effect'
                }
            },
            {
                'path': '/api/v1/glitch.gif',
                'description': 'Generate animated glitch text effect (GIF)',
                'method': 'GET',
                'params': {
                    'text': 'Text to display with glitch/corruption effect'
                }
            }
        ]
    }

@app.route('/api/v1/gradient-text')
def gradient_text():
    text = request.args.get('text', 'Hello, World!')
    try:
        image_data = generate_gradient_text(text)
        return send_file(
            image_data, 
            mimetype='image/png',
            download_name=f'gradient_{text[:30]}.png'
        )
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/v1/gradient-text.gif')
def animated_gradient_text():
    text = request.args.get('text', 'Hello, World!')
    try:
        image_data = generate_animated_gradient_text(text)
        return send_file(
            image_data, 
            mimetype='image/gif',
            download_name=f'gradient_{text[:30]}.gif'
        )
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/v1/neon')
def neon_text():
    text = request.args.get('text', 'Hello, World!')
    try:
        image_data = generate_neon_text(text)
        return send_file(image_data, mimetype='image/png')
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/v1/rainbow-wave')
def rainbow_wave_text():
    text = request.args.get('text', 'Hello, World!')
    try:
        image_data = generate_rainbow_wave(text)
        return send_file(image_data, mimetype='image/png')
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/v1/glitch.gif')
def glitch_text():
    text = request.args.get('text', 'Hello, World!')
    try:
        image_data = generate_glitch_text(text)
        return send_file(
            image_data, 
            mimetype='image/gif',
            download_name=f'glitch_{text[:30]}.gif'  # Add a proper filename
        )
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1754))
    app.run(host='0.0.0.0', port=port, debug=True) 