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
    def imgsrc(self):
        if self.image:
            return uploaded_images.url(f"characters/{self.id}/{self.image}")
        else:
            return None


class Log(db.Model):
    """ A character's journal entry for that day's campaign session """
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)
    membership_id = db.Column(db.Integer, db.ForeignKey('membership.id'), nullable=True)
    # TOGGLES
    public = db.Column(db.Boolean, default=False)    
    active = db.Column(db.Boolean(), default=True)
    # TIME
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    sesssion_on = db.Column(db.DateTime(), default=datetime.utcnow)
    published_on = db.Column(db.DateTime(), default=datetime.utcnow)
    sesssion_on = db.Column(db.DateTime(), default=datetime.utcnow)    
    # PROPS
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(80))
    link = db.Column(db.String(200))
    group = db.Column(db.Integer)
    sesssion = db.Column(db.DateTime(), default=datetime.utcnow) 
    # RELATIONSHIPS
    character = db.relationship('Character', back_populates='logs')
    campaign = db.relationship('Campaign', back_populates='logs')
    membership = db.relationship('Membership', back_populates='logs')


    def can_view(self, membership):
        """ returns True if a player is allowed to view a log entry."""
        return False