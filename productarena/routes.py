from productarena import app
from flask import render_template, redirect, url_for, flash, current_app, request
from productarena.models import Doctor 
from productarena import db
from productarena.forms import RegisterForm, LoginForm 
from flask_login import login_user, logout_user, login_required, current_user
import os
import secrets

 
@app.route('/home')
@login_required
def home_page():
    patients=[
    {'id':1, 'name':'Patient 1', 'symptoms':"Arm pain", 'time':"15:00"},
    {'id':2, 'name':'Patient 2', 'symptoms':"Leg pain", 'time':"15:00"}
    ]
    return render_template('home.html', patients = patients)
def save_images(photo):
    hash_photo=secrets.token_urlsafe(10)
    _, file_extenstion=os.path.splitext(photo.filename)
    photo_name=hash_photo + file_extenstion
    file_path=os.path.join(current_app.root_path,'static/images', photo_name)
    photo.save(file_path)
    return photo_name


@app.route('/register', methods=['GET','POST'])
def register_page():   
   form = RegisterForm()
   if form.validate_on_submit():
            photo = save_images(request.files.get('photo'))
            doctor_to_create =Doctor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_address=form.email_address.data,
            password=form.password1.data,
            image=photo
         )
            db.session.add(doctor_to_create)
            db.session.commit()
            return redirect(url_for('home_page'))
   if form.errors !={}:
         for err_msg in form.errors.values():
           flash(f'Error prilikom registracije: {err_msg}', category='danger')
            
   return render_template('register.html', form = form)
 
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user=Doctor.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
              login_user(attempted_user)
              return redirect(url_for('home_page'))

        else:
            flash(f'Pogrešan e-mail ili password: ', category='danger')
          
    return render_template('login.html', form=form)
 

@app.route('/logout')
def logout_page():
    logout_user()    
    return redirect (url_for('login_page'))


