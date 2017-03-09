from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
from DBModels.Data import *

def new_analysis():
    print (request.form['first-level'])
    print(request.form['second-level'])
    print(request.form['third-level'])
    data = request.form['workspace_name']
    print(data)
    return redirect(url_for('test'))