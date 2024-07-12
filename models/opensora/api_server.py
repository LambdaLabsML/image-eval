from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    num_frames = data.get('num_frames', '4s')
    resolution = data.get('resolution', '360p')
    aspect_ratio = data.get('aspect_ratio', '9:16')
    prompt = data.get('prompt', 'a beautiful waterfall')
    save_dir = os.environ.get('SAVE_DIR', '/workspace/Open-Sora/samples/samples')
    
    cmd = [
        'python', 'scripts/inference.py',
        'configs/opensora-v1-2/inference/sample.py',
        '--num-frames', num_frames,
        '--resolution', resolution,
        '--aspect-ratio', aspect_ratio,
        '--prompt', prompt,
        '--save-dir', save_dir
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return jsonify({'message': 'Image generation successful', 'save_dir': save_dir}), 200
    else:
        return jsonify({'message': 'Image generation failed', 'error': result.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
