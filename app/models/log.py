from .. import db, uploaded_images
from flask import flash
from flask_admin.contrib import sqla
from flask_security import UserMixin, RoleMixin, current_user, utils
from datetime import datetime
import humanize

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
    sesssion = db.Column(db.DateTime(), default=datetime.utcnow) # NIU
    published_on = db.Column(db.DateTime(), default=datetime.utcnow)    
    # PROPS
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(80))
    link = db.Column(db.String(200))
    group = db.Column(db.Integer)
    
    # RELATIONSHIPS
    character = db.relationship('Character', back_populates='logs')
    campaign = db.relationship('Campaign', back_populates='logs')
    membership = db.relationship('Membership', back_populates='logs')

    @property
    def img(self):
        """ Builds the path to the image stored in the static assets """
        return None

    def can_view(self, membership):
        """ returns True if a player is allowed to view a log entry."""
        if not membership or membership.campaign_id != self.campaign_id:
            return self.active and self.public and self.published_on != None
        log = self.campaign.get_logs_from_session(self.sesssion_on, membership=membership)
        if log:
            return log.group == self.group
        return True

    def can_edit(self, membership):
        """ Checks if the given membership has access to edit this log """
        if not membership or membership.campaign_id != self.campaign_id:
            return False
        # Will we ever allowed an editor to review log?
        return membership.isDM or membership.user_id==self.user_id

