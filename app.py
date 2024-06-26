from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from forms import RotateImageForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField, FloatField
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lfa0u4pAAAAAJpedooeLOUQXUqtNizbpRhMoDqj'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lfa0u4pAAAAAN5nkuLnrkCu752_7v_P7pcOi3Ef'

def save_plot(image_array, filename):
    plt.figure()
    plt.hist(image_array.ravel(), bins=256, color='blue', alpha=0.5)
    plt.xlabel('Значение пикселя')
    plt.ylabel('Количество')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def rotate_image(image, angle):
    return image.rotate(angle, expand=True)

def resize_image(image, scale):
    return image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))

class CaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RotateImageForm()
    captcha_form = CaptchaForm()

    if request.method == 'POST':
        if form.validate_on_submit() and captcha_form.validate_on_submit():
            image_file = request.files['image']
            angle = form.angle.data
            scale = form.scale.data
            image = Image.open(image_file)
            image = resize_image(image, scale)
            rotated_image = rotate_image(image, angle)
            rotated_image_array = np.array(rotated_image)

            original_histogram_path = 'static/original_histogram.png'
            rotated_histogram_path = 'static/rotated_histogram.png'
            save_plot(np.array(image), original_histogram_path)
            save_plot(rotated_image_array, rotated_histogram_path)

            rotated_image_path = 'static/rotated_image.png'
            resized_image_path = 'static/resized_image.png'
            rotated_image.save(rotated_image_path)

            return render_template('result.html', original_image=image_file.filename,
                                   rotated_image=rotated_image_path,
                                   resized_image=resized_image_path,
                                   original_histogram=original_histogram_path,
                                   rotated_histogram=rotated_histogram_path)
        else:
            flash('Ошибка. Пожалуйста, попробуйте снова.', 'danger')
    return render_template('index.html', form=form, captcha_form=captcha_form)

if __name__ == '__main__':
    app.run(debug=True)
