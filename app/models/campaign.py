from flask import flash
from flask_admin.contrib import sqla
from flask_security import UserMixin, RoleMixin, current_user, utils
from datetime import datetime
import humanize

# local imports
from .. import db, uploaded_images

class Campaign(db.Model):
    """ The adventure that a series of characters join """
    id = db.Column(db.Integer, primary_key=True)
    # PROPS
    active = db.Column(db.Boolean, default=True) # has it been archived / deleted
    live = db.Column(db.Boolean, default=True) # is the campaign still ongoing?
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    published_on = db.Column(db.DateTime(), default=None)
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    slug = db.Column(db.String(40))
    description = db.Column(db.Text)
    session_count = db.Column(db.Integer, default=0)
    image = db.Column(db.String(80))
    # RELATIONSHIPS
    memberships = db.relationship('Membership', backref='campaign')
    logs = db.relationship('Log', back_populates='campaign')

     # get the whole image path
    @property
    def img(self):
        if self.image:
            return uploaded_images.url(f"campaigns/{self.id}/{self.image}")
        else:
            return None

    def can_create_new_session(self, membership):
        """ Checks if the given membership is able to generate new blank log entries for all active characters """
        return membership and membership.campaign_id == self.id and membership.active and membership.isDM and self.active

    def get_logs_from_session(self, date, membership=None):
        """ Returns all logs that match the given date """
        logs = []
        if not membership:
            for log in self.logs:
                if log.session_on == date:
                    logs.append(log)
        else: 
            for log in self.logs:
                if log.session_on == date and log.membership_id == membership.id:
                    logs.append(log)
        return logs

    def get_list_of_sessions(self):
        """ Returns an array of dates showing each session meeting of the campagin """
        results = [] 
        for log in self.logs:
            if log.session_on not in results:
                results.append(log.session_on)
        return results

    def is_dm(self, requesting_user):
        """ Returns true or false depending on if the user is the DM of the campaign """

        return None
