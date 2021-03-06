import flask
from flask import request, jsonify, render_template
import boto3

app = flask.Flask(__name__)

app.config["DEBUG"] = True

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/index')
def index1():
   return render_template('index.html')

@app.route('/vms')
def vms():
   return render_template('vms.html')

@app.route('/users')
def users():
   return render_template('users.html')

@app.route('/inventory')
def inventory():
   return render_template('inventory.html')





app.run(host='0.0.0.0', port=80)
