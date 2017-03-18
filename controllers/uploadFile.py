import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import request, redirect, url_for, session
from werkzeug.utils import secure_filename
from DBModels.Data import *

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


