import os
from flask import request, redirect, url_for, session
from werkzeug.utils import secure_filename
from DBModels.Data import *
from DBModels.KBFile import *
from controllers.KnowledgeBaseCreation import *
import pandas as pd



def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8', keep_default_na=False)


# For a given file, return whether it's an allowed type or not
def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



def upload(directoryPath, ALLOWED_EXTENSIONS):
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup

        file.save(os.path.join(directoryPath, filename))
        insert_new_data(filename)
        return redirect(url_for('data_cleaning'))


def kbupload(directoryPath, ALLOWED_EXTENSIONS):
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        dirPath = os.path.join(directoryPath, filename)
        file.save(dirPath)
        insert_new_kbfile(filename)

        data_source = read_xlsx(dirPath)

        cnames = list(data_source)

        data = {}
        for name in cnames:
            data[name] = [x.lower() for x in list(filter(None, data_source[name].tolist()))]

        insert_new_kb_names(data)
        return redirect(url_for('knowledge_base'))

