import os
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Define the path using %APPDATA%
appdata_path = os.getenv('APPDATA')
script_path = os.path.join(appdata_path, "../Local/ov/pkg/audio2face-2023.2.0/exts/omni.audio2face.player/omni/audio2face/player/scripts/streaming_server/test_client.py")



#I need to further integrate the process into nvidia, for now we are just going to run a subprocess
@app.route('/upload_audio', methods=['POST'])
def receive_text():

    data = request.get_json()
    print(data)
    try:
        path = data['path']
        instance_name = data['instance_name']
        args = [path, instance_name]
        command = ['python', script_path] + args
        subprocess.run(command, check=True)
        return jsonify({'message': 'Text received', 'received_text': data}), 200
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(debug=True)