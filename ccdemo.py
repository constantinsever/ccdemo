import flask
from flask import request, jsonify, render_template
import boto3
from botocore.exceptions import ClientError
from subprocess import call
from flaskext.mysql import MySQL

import ansible_runner

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

#/change_instance_state?instanceID=i-0eb400ec9e5f08aea&newState=Reboot
@app.route('/change_instance_state',methods=['POST'])
def change_instance_state():
    result = "State change has been successfull"

    newState=request.form.get('newState')
    instance_id=request.form.get('instanceID')
   
    ec2 = boto3.client('ec2')

    if ( newState == 'Start'):
        try:
          response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        except ClientError as e:
          print(e)
          result = "State change exception, could not change state."
          
    elif ( newState == 'Stop'):
        try:
          response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        except ClientError as e:
          print(e)
          result = "State change exception, could not change state."


    elif ( newState == 'Reboot'):
        try:
          response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun=False)
        except ClientError as e:
          print(e)
          result = "State change exception, could not change state."

    
    return result

@app.route('/vms')
def vms():
   ec2 = boto3.resource('ec2', region_name='eu-west-1')

   filters = [{ 'Name': 'instance-state-name', 'Values': ['running','stopped','pending', 'shutting-down','terminated','stopping']}]
   instances=ec2.instances.filter(Filters=filters)

   return render_template('vms.html', instances=instances);


@app.route('/users')
def users():
   return render_template('users.html')

@app.route('/inventory')
def inventory():
   return render_template('inventory.html')

@app.route('/create_vm')
def create_vm():
   return render_template('create_vm.html')



@app.route('/create_vm_exec',methods=['POST'])
def create_vm_exec():
    instance_name=request.form.get('instance_name')
    os_image=request.form.get('lst_os_image')
    instance_type=request.form.get('lst_instance_type')
  
    import os
    curpath = os.path.abspath(os.curdir)

    f = open("ansible/create_vm_vars.yml", "w")
    f.write("instance_name: \"" + instance_name + "\"\n")
    f.write("instance_type: \"" + instance_type + "\"\n")
    f.write("ami_id: \"" + os_image + "\"\n")
    f.close()

    r = ansible_runner.run(playbook='/home/ccdemo/ccdemo/ansible/create_vm.yml')

    ec2 = boto3.resource('ec2', region_name='eu-west-1')

    filters = [{ 'Name': 'instance-state-name', 'Values': ['running','stopped','pending', 'shutting-down','terminated','stopping']}]
    instances=ec2.instances.filter(Filters=filters)

    return render_template('vms.html', instances=instances);




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
        <p><button type="button" class="btn btn-success">Create new template...</button></p>
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Template Name</th>
          <th align="center" nowrap="nowrap">AMI</th>
          <th align="center" nowrap="nowrap">CPU</th>
          <th align="center" nowrap="nowrap">RAM</th>
          <th align="center" nowrap="nowrap">Storage</th>
          <th align="center" nowrap="nowrap"></th>
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
          <td nowrap="nowrap" align="center"><img src="/static/images/settings.png" style="cursor:pointer" title="Settings"> &nbsp; <img src="/static/images/delete.png" style="cursor:pointer" title="Delete"></td>
         </tr>'''.format(record[0], record[1], record[2], record[3], record[4])

        result = header + rows + '</tbody></table>'

    
    if (inventory_type == "inventory_iso"):
        sql_query = "select * from inventory_iso"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <p><button type="button" class="btn btn-success">Add new ISO...</button></p>
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">ISO Image name</th>
          <th align="center" nowrap="nowrap">OS type</th>
          <th align="center" nowrap="nowrap">ISO file</th>
          <th align="center" nowrap="nowrap"></th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap" >{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap" align="center"><img src="/static/images/settings.png" style="cursor:pointer" title="Settings"> &nbsp; <img src="/static/images/delete.png" style="cursor:pointer" title="Delete"></td>
         </tr>'''.format(record[0], record[1], record[2])

        result = header + rows + '</tbody></table>'


    if (inventory_type == "inventory_apps"):
        sql_query = "select * from inventory_apps"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <p><button type="button" class="btn btn-success">Add new application...</button></p>
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Application name</th>
          <th align="center" nowrap="nowrap">OS type</th>
          <th align="center" nowrap="nowrap">Installation file</th>
          <th align="center" nowrap="nowrap">Notes</th>
          <th align="center" nowrap="nowrap"></th>
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
          <td nowrap="nowrap" align="center"><img src="/static/images/settings.png" style="cursor:pointer" title="Settings"> &nbsp; <img src="/static/images/delete.png" style="cursor:pointer" title="Delete"></td>
         </tr>'''.format(record[0], record[1], record[2], record[3])

        result = header + rows + '</tbody></table>'


    if (inventory_type == "inventory_ansible"):
        sql_query = "select * from inventory_ansible"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <p><button type="button" class="btn btn-success">Add new Ansible Playbook ...</button></p>        
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Playbook name</th>
          <th align="center" nowrap="nowrap">Description</th>
          <th align="center" nowrap="nowrap">Run command</th>
          <th align="center" nowrap="nowrap"></th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap" align="center"><img src="/static/images/settings.png" style="cursor:pointer" title="Settings"> &nbsp; <img src="/static/images/delete.png" style="cursor:pointer" title="Delete"></td>
         </tr>'''.format(record[0], record[1], record[2])

        result = header + rows + '</tbody></table>'


    if (inventory_type == "inventory_tf"):
        sql_query = "select * from inventory_tf"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <p><button type="button" class="btn btn-success">Add new Terraform script...</button></p>        
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th nowrap="nowrap">Script name</th>
          <th align="center" nowrap="nowrap">Description</th>
          <th align="center" nowrap="nowrap">Cloud provider</th>
          <th align="center" nowrap="nowrap">Script file</th>
          <th align="center" nowrap="nowrap"></th>
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
          <td nowrap="nowrap" align="center"><img src="/static/images/settings.png" style="cursor:pointer" title="Settings"> &nbsp; <img src="/static/images/delete.png" style="cursor:pointer" title="Delete"></td>
         </tr>'''.format(record[0], record[1], record[2], record[3])

        result = header + rows + '</tbody></table>'

    if (inventory_type == "inventory_startup"):
        sql_query = "select * from inventory_startup"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <p><button type="button" class="btn btn-success">Add new Startup script ...</button></p>
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th align="center" nowrap="nowrap">Script name</th>
          <th align="center" nowrap="nowrap">Description</th>
          <th align="center" nowrap="nowrap">Script command</th>
          <th align="center" nowrap="nowrap"></th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap" align="center"><img src="/static/images/settings.png" style="cursor:pointer" title="Settings"> &nbsp; <img src="/static/images/delete.png" style="cursor:pointer" title="Delete"></td>
         </tr>'''.format(record[0], record[1], record[2])

        result = header + rows + '</tbody></table>'






    if (inventory_type == "inventory_docker"):
        sql_query = "select * from inventory_docker"
        cursor.execute(sql_query)

        res = cursor.fetchall()

        header = '''
        <p><button type="button" class="btn btn-success">Add new Docker image ...</button></p>        
        <table class="table table-hover table-bordered">
        <thead>
         <tr>
          <th align="center" nowrap="nowrap">Image name</th>
          <th align="center" nowrap="nowrap">Description</th>
          <th align="center" nowrap="nowrap"></th>
        </tr>
       </thead>
       <tbody>'''

        rows = ""

        for record in res:
         rows = rows + ''' <tr>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap">{}</td>
          <td nowrap="nowrap" align="center"><img src="/static/images/settings.png" style="cursor:pointer" title="Settings"> &nbsp; <img src="/static/images/delete.png" style="cursor:pointer" title="Delete"></td>
         </tr>'''.format(record[0], record[1])

        result = header + rows + '</tbody></table>'



   
    cursor.close()    
    conn.close()

    return result



app.run(host='0.0.0.0', port=5000)
