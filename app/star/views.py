# library imports
from flask import render_template, redirect, flash, url_for, session, request, current_app, send_from_directory
from flask_security import login_required, roles_required, current_user
from flask_uploads import UploadNotAllowed
from flask_mail import Message
from slugify import slugify
import os
# our objects
from . import star as app
from .. import db, uploaded_images, mail
from ..models import Post, Tag, User, Character, Log, Membership, Campaign



###########################
###### LOG ROUTES
###########################
@app.route('/log/<int:log_id>')
@login_required
def view_log(log_id):
    log = Log.query.filter_by(active=True, id=log_id).first_or_404()
    return render_template('star/log.html', log=log)

@app.route('/log/new', methods=('GET', 'POST'))
@login_required
@roles_required('end_user')
def new_log():
    form = LogForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded", 'danger')
        '''
        # tags have been disabled
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            tag = new_tag
        else:
            tag = form.tag.data
        '''
        title = form.title.data
        subtitle = form.subtitle.data
        body = form.body.data
        group = form.group.data
        # slug = slugify(title)
        log = Log(current_user, title, subtitle, body, group, image=filename)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('star.view_read', slug=slug))
    return render_template('star/log.html', form=form, action="new")
    
@app.route('/log/edit/<int:log_id>', methods=('GET', 'POST'))
@roles_required('end_user')
def edit_log(log_id):
    log = Log.query.filter_by(id=log_id).first_or_404()
    form = LogForm(obj=log)
    filename = None
    if form.validate_on_submit():
        original_image = log.image
        form.populate_obj(log)
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded")
            if filename:
                log.image = filename
        else:
            log.image = original_image
        '''
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            post.tag = new_tag
        '''
        db.session.commit()
        return redirect(url_for('read', slug=log.slug))
    return render_template('main/log.html', form=form, log=log, action="edit")

@app.route('/log/delete/<int:log_id>')
@roles_required('end_user')
def delete_log(log_id):
    log = Log.query.filter_by(id=log_id).first_or_404()
    log.active = False
    db.session.commit()
    flash("Log deleted", 'success')
    return redirect(url_for('log_index'))


###########################
###### CHARACTER ROUTES
###########################
@app.route('/character/<int:character_id>')
def view_character(character_id):
    character = Character.query.filter_by(active=True, id=character_id).first_or_404()
    return render_template('star/character.html', character=character)

@app.route('/character/new', methods=('GET', 'POST'))
@login_required
# @roles_required('end_user')
def new_character():
    form = CharacterForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded", 'danger')
        '''
        # tags have been disabled
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            tag = new_tag
        else:
            tag = form.tag.data
        '''
        name = form.name.data
        description = form.description.data
        link = form.link.data
        hp = form.hp.data
        stre = form.str.data
        inte = form.int.data
        wis = form.wis.data
        cons = form.cons.data
        # slug = slugify(title)
        character = Character(current_user, name, description, link, hp, stre, inte, wis, cons, image=filename)
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('read', slug=slug))
    return render_template('main/character.html', form=form, action="new")
    
@app.route('/character/edit/<int:character_id>', methods=('GET', 'POST'))
# @roles_required('end_user')
def edit_character(character_id):
    character = Character.query.filter_by(id=character_id).first_or_404()
    form = CharacterForm(obj=character)
    filename = None
    if form.validate_on_submit():
        original_image = character.image
        form.populate_obj(character)
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded")
            if filename:
                character.image = filename
        else:
            character.image = original_image
        '''
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            post.tag = new_tag
        '''
        db.session.commit()
        return redirect(url_for('read', slug=character.slug))
    return render_template('main/character.html', form=form, character=character, action="edit")

@app.route('/character/delete/<int:character_id>')
@roles_required('end_user')
def delete_character(character_id):
    character = Character.query.filter_by(id=character_id).first_or_404()
    character.active = False
    db.session.commit()
    flash("Character deleted", 'success')
    return redirect(url_for('character_index'))


###########################
# CAMPAIGN ROUTES
###########################
@app.route('/campaign/<int:campaign_id>')
def view_campaign(campaign_id):
    campaign = Campaign.query.filter_by(active=True, id=campaign_id).first_or_404()
    return render_template('star/campaign.html', campaign=campaign)

@app.route('/campaign/new', methods=('GET', 'POST'))
@login_required
@roles_required('end_user')
def new_campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded", 'danger')
        '''
        # tags have been disabled
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            tag = new_tag
        else:
            tag = form.tag.data
        '''
        title = form.title.data
        subtitle = form.subtitle.data
        description = form.description.data
        slug = slugify(title)
        campaign = Campaign(current_user, title, subtitle, description, slug, session_count, image=filename)
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('read', slug=slug))
    return render_template('main/campaign.html', form=form, action="new")
    
@app.route('/campaign/edit/<int:campaign_id>', methods=('GET', 'POST'))
@roles_required('admin')
def edit_campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first_or_404()
    form = CampaignForm(obj=campaign)
    filename = None
    if form.validate_on_submit():
        original_image = campaign.image
        form.populate_obj(campaign)
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded")
            if filename:
                campaign.image = filename
        else:
            campaign.image = original_image
        '''
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            post.tag = new_tag
        '''
        db.session.commit()
        return redirect(url_for('read', slug=campaign.slug))
    return render_template('main/campaign.html', form=form, campaign=campaign, action="edit")

@app.route('/campaign/delete/<int:campaign_id>')
@roles_required('admin')
def delete_campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first_or_404()
    campaign.live = False
    db.session.commit()
    flash("Article deleted", 'success')
    return redirect(url_for('campaign_index'))


###########################
###### OTHER ROUTES
###########################
@app.route('/dashboard')
@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('star/dashboard.html')
