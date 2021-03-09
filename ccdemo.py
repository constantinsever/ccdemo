import flask
from flask import request, jsonify, render_template
import boto3
from subprocess import call
from flaskext.mysql import MySQL


app = flask.Flask(__name__)


mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'ccdemo'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ccdemo'
app.config['MYSQL_DATABASE_DB'] = 'ccdemo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




app.config["DEBUG"] = True

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/index')
def index1():
   return render_template('index.html')

@app.route('/vms')
def vms():
#  client = boto3.client('ec2')
#  responses = client.stop_instances(
#    InstanceIds=['i-0eb400ec9e5f08aea'],
#    DryRun=False #!!!
#   )
#  return jsonify(responses)
  return render_template('vms.html')

@app.route('/users')
def users():
   return render_template('users.html')

@app.route('/inventory')
def inventory():
   return render_template('inventory.html')


@app.route('/show_inventory/<inventory_type>')
def show_inventory(inventory_type):
    conn = mysql.connect()
    cursor = conn.cursor()

    result = ""

    if (inventory_type == "inventory_templates"):
        sql_query = "select * from inventory_templates"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Template Name</th>
          <th align="center" nowrap="nowrap">AMI</th>
          <th align="center" nowrap="nowrap">CPU</th>
          <th align="center" nowrap="nowrap">RAM</th>
          <th align="center" nowrap="nowrap">Storage</th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
         </tr>'''.format(record[0], record[1], record[2], record[3], record[4])

        result = header + rows + '</tbody></table>'

    
    if (inventory_type == "inventory_iso"):
        sql_query = "select * from inventory_iso"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">ISO Image name</th>
          <th align="center" nowrap="nowrap">OS type</th>
          <th align="center" nowrap="nowrap">ISO file</th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap">{}</td>
         </tr>'''.format(record[0], record[1], record[2])

        result = header + rows + '</tbody></table>'


    if (inventory_type == "inventory_apps"):
        sql_query = "select * from inventory_apps"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Application name</th>
          <th align="center" nowrap="nowrap">OS type</th>
          <th align="center" nowrap="nowrap">Installation file</th>
          <th align="center" nowrap="nowrap">Notes</th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
         </tr>'''.format(record[0], record[1], record[2], record[3])

        result = header + rows + '</tbody></table>'


    if (inventory_type == "inventory_ansible"):
        sql_query = "select * from inventory_ansible"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Playbook name</th>
          <th align="center" nowrap="nowrap">Description</th>
          <th align="center" nowrap="nowrap">Run command</th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
         </tr>'''.format(record[0], record[1], record[2])

        result = header + rows + '</tbody></table>'


    if (inventory_type == "inventory_tf"):
        sql_query = "select * from inventory_tf"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Script name</th>
          <th align="center" nowrap="nowrap">Description</th>
          <th align="center" nowrap="nowrap">Cloud provider</th>
          <th align="center" nowrap="nowrap">Script file</th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
         </tr>'''.format(record[0], record[1], record[2], record[3])

        result = header + rows + '</tbody></table>'




   
    cursor.close()    
    conn.close()

    return result



app.run(host='0.0.0.0', port=5000)
