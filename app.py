from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import os
import shutil

app = Flask(__name__)

upload_dir = 'upload'
result_dir = 'result'
detected_dir = 'runs/detect'

model = YOLO("yolo12n.pt")

def initialize_directories():
    for directory in [upload_dir, result_dir, detected_dir]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

initialize_directories()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        if file.filename == "":
            return 'No selected file'
        
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(upload_dir, filename)
            file.save(upload_path)

            # ディレクトリを削除
            if os.path.exists(detected_dir):
                shutil.rmtree(detected_dir)

            # YOLOモデルを実行 (推論結果を保存)
            results = model(upload_path, save=True, save_txt=True)

            # 推論結果が保存されるパスを変数に定義
            detect_predict_dir = os.path.join(detected_dir, 'predict')

            # フォルダ内のファイルを取得
            all_files = os.listdir(detect_predict_dir)
            predicted_files = [f for f in all_files if os.path.isfile(os.path.join(detect_predict_dir, f))]

            # 推論後のファイルを移動
            predicted_filename = predicted_files[0]
            predicted_path = os.path.join(detect_predict_dir, predicted_filename)
            destination_path = os.path.join(result_dir, predicted_filename)
            shutil.move(predicted_path, destination_path)

            # 表示ページへ
            return render_template('display.html', user_image=predicted_filename)

    return render_template('upload.html')

@app.route('/display/<filename>')
def display_file(filename):
    """result/ フォルダのファイルを表示"""
    return send_from_directory(result_dir, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
