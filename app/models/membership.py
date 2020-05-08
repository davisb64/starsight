from flask import flash
from flask_admin.contrib import sqla
from flask_security import UserMixin, RoleMixin, current_user, utils
from datetime import datetime
import humanize

# local imports
from .. import db, uploaded_images


class Membership(db.Model):
    """ Qualified association object between campaign and character """
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)
    # TOGGLES
    isDM = db.Column(db.Boolean, default=False)    
    active = db.Column(db.Boolean(), default=True)
    # TIME
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    # RELATIONSHIPS (backref: user, campaign)
    character = db.relationship('Character', back_populates='memberships')
    logs = db.relationship('Log', back_populates='membership')

    def get_most_recent_log(self):
        """ Returns the most recently written log """
        return None

    def can_deactivate(self, membership):
        """ Checks if the given membership has the authority to 'delete' this membership """
        return None
