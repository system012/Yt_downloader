from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class DownloadForm(FlaskForm):
    link = StringField('Youtube link')
    submit = SubmitField('Download')
    tar = SubmitField('Download TAR')
