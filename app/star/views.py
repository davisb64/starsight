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
from ..models import Post, Tag, User

# LOG ROUTES

@app.route('/log')
@app.route('/log/')
def log_index():
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc())
    return render_template('star/log.html', posts=posts)

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
        slug = slugify(title)
        log = Log(current_user, title, subtitle, body, slug, image=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('read', slug=slug))
    return render_template('main/log.html', form=form, action="new")
    
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
    return render_template('main/post.html', form=form, log=log, action="edit")

@app.route('/log/delete/<int:post_id>')
@roles_required('end_user')
def delete_log(log_id):
    log = Log.query.filter_by(id=log_id).first_or_404()
    log.live = False
    db.session.commit()
    flash("Log deleted", 'success')
    return redirect(url_for('log_index'))

# CHARACTER ROUTES

@app.route('/character')
@app.route('/character/')
def character_index():
    characters = Character.query.filter_by(live=True).order_by(Character.publish_date.desc())
    return render_template('star/character.html', characters=characters)

@app.route('/character/new', methods=('GET', 'POST'))
@login_required
@roles_required('end_user')
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
        title = form.title.data
        subtitle = form.subtitle.data
        body = form.body.data
        slug = slugify(title)
        character = Character(current_user, title, subtitle, body, slug, image=filename)
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('read', slug=slug))
    return render_template('main/character.html', form=form, action="new")
    
@app.route('/character/edit/<int:character_id>', methods=('GET', 'POST'))
@roles_required('end_user')
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
        return redirect(url_for('read', slug=post.slug))
    return render_template('main/post.html', form=form, character=character, action="edit")

@app.route('/character/delete/<int:character_id>')
@roles_required('end_user')
def delete_character(character_id):
    character = Character.query.filter_by(id=character_id).first_or_404()
    character.live = False
    db.session.commit()
    flash("Character deleted", 'success')
    return redirect(url_for('blog_index'))

# CAMPAIGN ROUTES

@app.route('/campaign')
@app.route('/campaign/')
def campaign_index():
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc())
    return render_template('main/blog.html', posts=posts)

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
        body = form.body.data
        slug = slugify(title)
        post = Post(current_user, title, subtitle, body, slug, image=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('read', slug=slug))
    return render_template('main/post.html', form=form, action="new")
    
@app.route('/blog/edit/<int:post_id>', methods=('GET', 'POST'))
@roles_required('admin')
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)
    filename = None
    if form.validate_on_submit():
        original_image = post.image
        form.populate_obj(post)
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded")
            if filename:
                post.image = filename
        else:
            post.image = original_image
        '''
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            post.tag = new_tag
        '''
        db.session.commit()
        return redirect(url_for('read', slug=post.slug))
    return render_template('main/post.html', form=form, post=post, action="edit")

@app.route('/blog/delete/<int:post_id>')
@roles_required('admin')
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article deleted", 'success')
    return redirect(url_for('blog_index'))

