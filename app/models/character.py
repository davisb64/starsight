from .. import db, uploaded_images
from flask import flash
from flask_admin.contrib import sqla
from flask_security import UserMixin, RoleMixin, current_user, utils
from datetime import datetime
import humanize


class Character(db.Model):
    """ Stats tracker for a user's fictional character """
    # KEYS
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # PROPS
    active = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    name = db.Column(db.String(80))
    link = db.Column(db.String(200))
    description = db.Column(db.Text)
    # RELATIONSHIPS user backref
    memberships = db.relationship('Membership', back_populates='character')
    logs = db.relationship('Log', back_populates='character')
    image = db.Column(db.String(80))

    def __init__(*args):
        if args.get('name', False):
          self.name = args['name']  
        if args.get('link', False):
          self.link = args['link']
    
    # get the whole image path
    @property
    def img(self):
        if self.image:
            return uploaded_images.url(f"characters/{self.id}/{self.image}")
        else:
            return None

    def get_earliest_session(self):
        """ Searches all log entries to find the earliest posted date """
        return None

