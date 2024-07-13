from flask import Flask, request, jsonify, send_file
import subprocess
import os
import logging
import glob

app = Flask(__name__)

# Configure logging to file
logging.basicConfig(filename='/data/api_server.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/generate', methods=['POST'])
def generate_image():


    try:
        data = request.json
        num_frames = data.get('num_frames', '4s')
        resolution = data.get('resolution', '360p')
        aspect_ratio = data.get('aspect_ratio', '9:16')
        prompt = data.get('prompt', 'a beautiful waterfall')
        save_dir = os.environ.get('SAVE_DIR', '/data')  

        # Remove files with name pattern `sample_*.mp4`
        for file_path in glob.glob(os.path.join(save_dir, 'sample_*.mp4')):
            os.remove(file_path)
            logging.debug(f"Removed file: {file_path}")
        
        cmd = [
            'python', 'scripts/inference.py',
            'configs/opensora-v1-2/inference/sample.py',
            '--num-frames', num_frames,
            '--resolution', resolution,
            '--aspect-ratio', aspect_ratio,
            '--prompt', prompt,
            '--save-dir', save_dir
        ]

        logging.debug(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        logging.debug(f"Command output: {result.stdout}")  
        logging.error(f"Command error output: {result.stderr}")
        
        if result.returncode == 0:
            # Assuming the generated file is saved in the save_dir with a known name
            generated_file_path = os.path.join(save_dir, 'sample_0000.mp4')  # Update this with the correct filename
            if os.path.exists(generated_file_path):
                return send_file(generated_file_path, as_attachment=True)
            else:
                logging.error(f"Generated file not found: {generated_file_path}")
                return jsonify({'message': 'Image generation successful, but file not found', 'save_dir': save_dir}), 200
        else:
            logging.error("Image generation failed")
            return jsonify({'message': 'Image generation failed', 'error': result.stderr}), 500
    except Exception as e:
        logging.exception("An unexpected error occurred")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)