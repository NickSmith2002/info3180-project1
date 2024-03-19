"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from .models import Property, NewPropertyForm
from . import db
from werkzeug.utils import secure_filename
from flask import send_from_directory


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Nicholas Smith")


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

#Create Property Page
@app.route('/properties/create', methods=['GET', 'POST'])
def create():
    form = NewPropertyForm()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        location = request.form['location']
        price = request.form['price']
        p_type = request.form['type']
        p_photo = request.files['photo']
        file = secure_filename(p_photo.filename)
        p_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
        new_property = Property(title=title, description=description, bedrooms=bedrooms, bathrooms=bathrooms, location=location, price=price, type=p_type, photo=file)
        db.session.add(new_property)
        db.session.commit()
        flash('Property added successfully', 'success')
        return redirect(url_for('properties'))
    return render_template('create.html',form=form)

@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/<propertyid>')
def property(propertyid):
    property = Property.query.get(propertyid)
    return render_template('property.html', property=property)

@app.route('/uploads/<filename>')
def uploaded_images(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)