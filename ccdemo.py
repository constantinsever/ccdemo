aaaimport flask
from flask import request, jsonify, render_template
import boto3

app = flask.Flask(__name__)

app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'}
]



@app.route('/')
def index():
   return render_template('index.html')


app.run(host='0.0.0.0', port=80)
