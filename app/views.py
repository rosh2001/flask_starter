"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import os
import locale
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import AddProperty
from app.models import Property
from werkzeug.utils import secure_filename
locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
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
    return render_template('about.html', name="RoShaun Young")


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

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route('/properties/create', methods =['GET', 'POST'])
def addproperty():
    formobject =  AddProperty()

    if request.method == 'GET':
        return render_template('addproperty.html', formobj = formobject)


    if request.method == 'POST':
        if formobject.validate_on_submit(): 
            fileobj = request.files['photo']
            cleanedname = secure_filename(fileobj.filename)
            fileobj.save(os.path.join(app.config['UPLOAD_FOLDER'], cleanedname))
            if fileobj and cleanedname != "" :
                newproperty = Property(request.form['propertytitle'],request.form['numberofrooms'], request.form['numberofbathrooms'], request.form['location'], request.form['price'], request.form['description'], request.form['Type'], cleanedname)
                db.session.add(newproperty)
                db.session.commit()
                flash('Your Property Was Successfully Added', 'success')
                return redirect(url_for('displayproperties'))
    flash_errors(formobject) 
    return render_template('addproperty.html', formobj = formobject)


@app.route('/properties')
def displayproperties():
   if request.method == 'GET':
       properties = Property.query.all()
       return render_template('properties.html', propertylist = properties, loc =locale)


@app.route('/properties/<propertyid>')
def displayproperty(propertyid):
    property = Property.query.filter(Property.id==propertyid).all()[0]
    
    if property.numberofrooms > 1:
        bedroomlabel = 'Bedrooms'
    else:
        bedroomlabel = 'Bedroom'

    if property.numberofbathrooms > 1:
        bathroomlabel ='Bathrooms'
    else:
        bathroomlabel ='Bathroom'
    
    return render_template('property.html', singleproperty = property, bathlabel = bathroomlabel, bedlabel = bedroomlabel, loc=locale)

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


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
