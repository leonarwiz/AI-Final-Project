from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import subprocess
import cv2

app = Flask(__name__)

# Set where you want the images to be uploaded
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Color configs
color_config = {"black": 1, "blonde": 2, "brown": 3}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        selected_features = color_config[request.form.get('hairColor')]

        # Create Directory
        path1 = './input'
        path2 = './input/Black_Hair'
        if not os.path.isdir(path2):
            if not os.path.isdir(path1):
                os.mkdir(path1)
            os.mkdir(path2)

        # Save image
        file_suffix = os.path.splitext(f.filename)[1]
        save_path = path2 + "/in" + file_suffix
        f.save(save_path)

        # Run model
        cmd = "python main.py --mode test --dataset RaFD --image_size 128 --c_dim 3 --sample_dir stargan_celeba/samples --log_dir stargan_celeba/logs --model_save_dir stargan_celeba/models --result_dir static/output --selected_attrs Black_Hair Blond_Hair Brown_Hair --test_iters 50000 --test_iters 50000 --rafd_image_dir input"
        subprocess.run(cmd.split())
        os.remove(save_path)

        # Process generated image
        img = cv2.imread("./static/output/1-images.jpg")
        img = img[0:128, selected_features * 128: (selected_features+1) * 128]
        cv2.imwrite("./static/output/1-images.jpg", img)

        # Return the relative path
        out_path = "./output/1-images.jpg"

        # rel_path = os.path.join('uploads', filename)
        return render_template('result.html', image_path=out_path)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
