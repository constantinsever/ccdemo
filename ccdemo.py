import flask
from flask import request, jsonify, render_template
import boto3
from subprocess import call


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
  client = boto3.client('ec2')
  responses = client.stop_instances(
    InstanceIds=['i-0eb400ec9e5f08aea'],
    DryRun=False #!!!
   )
  return jsonify(responses)
#  return render_template('vms.html')

@app.route('/users')
def users():
   return render_template('users.html')

@app.route('/inventory')
def inventory():
    call(["ansible-playbook", "ansible/ccdemo.yml"])
    return "done"
#   return render_template('inventory.html')





app.run(host='0.0.0.0', port=5000)
