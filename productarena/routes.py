from productarena import app
from flask import render_template
from productarena.models import Doctor 
from productarena import db


 
@app.route('/home')

def home_page():
   
   return render_template('home.html')
 

