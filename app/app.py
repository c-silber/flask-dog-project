# IMPORTS
from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from filters import datetimeformat, file_type
from resources import get_bucket, get_buckets_list, add_tags_to_object, get_detail_bucket_list
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from config import S3_BUCKET
import requests

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        'Dog Breed Classifier',
        View('Home', 'index'),
		View('Files', 'files'),
    )

# CONFIG
app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)
nav.init_app(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		file = request.files['user_file']
		my_bucket = get_bucket()
		my_bucket.Object(file.filename).put(Body=file)
		flash('File uploaded successfully')
		return redirect(url_for('files'))

	return render_template('index.html')

@app.route('/files', methods=['GET', 'POST'])
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()
    objects = get_detail_bucket_list()

    return render_template('files.html', my_bucket=my_bucket, files=objects)

@app.route('/files/<id>', methods=['POST'])
def getDogBreedFromUrl(id):
    print(id)

    url = 'https://s3.amazonaws.com/' + S3_BUCKET + '/' + id;
    params = {'imagePath':url}
    print(params)

    apiUrl = 'http://172.104.212.211:8000/getDogBreed'

    r = requests.post(url=apiUrl, params=params)
    data = r.json()
    print(data)

    my_bucket = get_bucket()
    add_tags_to_object(id, url, data['type'], data['breed'])
    objects = get_detail_bucket_list()

    return render_template('files.html', my_bucket=my_bucket, files=objects)

if __name__ == '__main__':
    app.run(debug=True)
