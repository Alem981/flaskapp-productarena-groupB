from productarena import app
from datetime import datetime, date, timedelta
from flask import render_template, redirect, url_for, flash, current_app, request
from productarena.models import Doctor, Patient 
from productarena import db
from productarena.forms import RegisterForm, LoginForm, AddPatientForm
from flask_login import login_user, logout_user, login_required, current_user
import os
import secrets
import datetime as dt

 
@app.route('/home')
@login_required
def home_page():
    today = dt.date.today()  
    patients=Patient.query.filter_by(date=today).all()
    tomorrow=dt.date.today()+timedelta(days=1)
    patients_tomorrow = Patient.query.filter_by(date=tomorrow).all()

    after_tomorrow=dt.date.today()+timedelta(days=2)
    patients_after_tomorrow = Patient.query.filter_by(date=after_tomorrow).all()
    
    all_patients=Patient.query.all()


    return render_template('home.html', patients = patients, patients_tomorrow=patients_tomorrow, patients_after_tomorrow=patients_after_tomorrow, all_patients=all_patients)
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


@app.route('/add_patient', methods=['GET','POST'])
def add_patient_page():   
   form = AddPatientForm()
   if form.validate_on_submit():
            photo = save_images(request.files.get('photo'))
            patient_to_create =Patient(
            username=form.username.data, 
            symptoms=form.symptoms.data, 
            date=form.date.data,         
            time=form.time.data,  
            image=photo
         )
            db.session.add(patient_to_create)
            db.session.commit()
            return redirect(url_for('home_page'))
   if form.errors !={}:
         for err_msg in form.errors.values():
           flash(f'Error prilikom registracije: {err_msg}', category='danger')
            
   return render_template('add_patient.html', form = form)
 
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


