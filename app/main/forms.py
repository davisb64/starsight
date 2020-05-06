from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, TelField
from wtforms import validators, StringField, PasswordField, TextAreaField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField
from ..models import Tag
from flask_security.forms import RegisterForm, ConfirmRegisterForm
from .. import db

# This queues up all tags with no regard who made them
def tags():
    return Tag.query


class ExtendedRegisterForm(ConfirmRegisterForm):
    first_name = StringField('First Name', [validators.Required()])
    last_name = StringField('Last Name', [validators.Required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])
        
    def validate(self):
        success = True
        if not super(ExtendedRegisterForm, self).validate():
            success = False
        return success
    

# We can make our own validators
def CheckNameLength(form, field):
  if len(field.data) < 4:
    raise validators.ValidationError('Name must have more then 3 characters')

class PostForm(FlaskForm):
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    title = StringField('Title', [
            validators.Required(),
            validators.Length(max=80)])
    subtitle = StringField('Subtitle', [
            validators.Required(),
            validators.Length(max=80)])        
    body = CKEditorField('Content', validators=[validators.Required()])
    # tag = QuerySelectField('Tag', query_factory=tags, validators=[validators.Required()])
    # new_tag = StringField('New Tag')
    
class ContactForm(FlaskForm):
    """ Optional contact form for home page """
    name = StringField('Your Name:', [validators.DataRequired(), CheckNameLength])
    email = StringField('Your e-mail address:', [validators.DataRequired(), validators.Email('your@email.com')])
    message = TextAreaField('Your message:', [validators.DataRequired()])
    submit = SubmitField('Send Message')


class SettingsForm(FlaskForm):
    """ Modify a user's details and options """
    first_name = StringField('First Name', [validators.Required()])
    last_name = StringField('Last Name', [validators.Required()])
    about = TextAreaField('About me',[validators.Optional()])
    address = TextAreaField('Address',[validators.Optional()])
    phone = TelField('Phone number',[validators.Optional()])
    # TODO: add file size validator
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])


class CampaignForm(FlaskForm):
    """ Modify a campaign's details and options """
    title = StringField('Campaign Title', [validators.Required()])
    subtitle = StringField('Campaign Subtitle', [validators.Optional()])
    description = TextAreaField('About Campaign',[validators.Optional()])
    # TODO: add file size validator
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])


class LogForm(FlaskForm):
    """ Modify a log's details and options """
    title = StringField('Log Title', [validators.Required()])
    subtitle = StringField('Log Subtitle', [validators.Optional()])
    character_sheet = StringField('Link to character sheet', [validators.Optional()])
    body = TextAreaField('Log Body',[validators.Optional()])
    group = IntegerField('Log Group Number',[validators.Optional()])
    # TODO: add file size validator
    image = FileField('Log Image', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])

class CharacterForm(FlaskForm):
    """ Modify a log's details and options """
    name = StringField('Character Name', [validators.Required()])
    description = TextAreaField('Character Description',[validators.Optional()])
    character_sheet = StringField('Link to character sheet', [validators.Optional()])
    # TODO: add file size validator
    image = FileField('Character Image', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
