from productarena import app
from flask import render_template, redirect, url_for, flash
from productarena.models import Doctor 
from productarena import db
from productarena.forms import RegisterForm, LoginForm
from flask_login import login_user


 
@app.route('/home')
@app.route('/')
def home_page():   
   return render_template('home.html')
 

@app.route('/register', methods=['GET','POST'])
def register_page():   
   form = RegisterForm()
   if form.validate_on_submit():
         doctor_to_create =Doctor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_address=form.email_address.data,
            password=form.password1.data
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