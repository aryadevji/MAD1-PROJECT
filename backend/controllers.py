from flask import Flask,render_template, current_app as app, request, flash, redirect
import os
from .models import *
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/login',methods=["GET","POST"])
def index():
    if request.method=="POST":
        user_name=request.form.get("loginusername")
        password=request.form.get("loginpassword")
        urole=request.form.get("loginrole")

        if not user_name or not password or not urole:
            flash("Please fill out all fields", category="Failed")
            return render_template('login.html')
        
        usr = Users.query.filter_by(username=user_name, role=urole).first()
        if usr is None:
            flash("User does not exists", category="Failed")  #credintals not empty
            return render_template('login.html')

        if not check_password_hash(usr.passhash, password):
            flash("Invalid Password", category="Failed")  #password verification
            return render_template('login.html')

        if usr.role == 0:                                #login based on role
            return render_template("admin-home.html")
        elif usr.role == 1:
            return render_template("customer-home.html")
        elif usr.role == 2:
            return render_template("professional-home.html")
            
         
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register-customer',methods=["GET","POST"])
def register_customer():
    # if request.method=="POST":

    return render_template('register-customer.html')

@app.route('/register-professional',methods=["GET","POST"])
def register_professional():
    if request.method=="POST":
        full_name=request.form.get("profname")
        prof_email=request.form.get("profemail")
        user_name=request.form.get("profusername")
        password=request.form.get("profpassword")
        service_name=request.form.get("servicename")
        prof_exprience=request.form.get("exprience")
        prof_add=request.form.get("profadd")
        prof_pincode=request.form.get("profpincode")

        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, browser submits an empty part without a filename
        if file.filename == '':
            flash("No selected file", category="error")
            return redirect(request.url)

        # Directly check the file extension here
        if file.filename.endswith('.pdf'):
            # Secure the filename
            filename = secure_filename(file.filename)
            
            # Define the path to save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file to the specified directory
            file.save(file_path)
            
            # Save the file path to the database
            new_professional = Professional(name=full_name, email=prof_email,pincode=prof_pincode,address=prof_add,service=service_name,exprience=prof_exprience,attachment=file_path)
            prof_user = Users(username=user_name,passhash=generate_password_hash(password, method='pbkdf2:sha256'),role=2)
            db.session.add(new_professional)
            db.session.commit()


    return render_template('register-professional.html')


@app.route('/professional-home',methods=["GET","POST"])
def professional_home():
    # if request.method=="POST":
        #do someting
    return render_template('professional-home.html')

@app.route('/professional-search',methods=["GET","POST"])
def professional_search():
    # if request.method=="POST":
        #do someting
    return render_template('professional-search.html')

@app.route('/professional-summary',methods=["GET","POST"])
def professional_summary():
    # if request.method=="POST":
        #do someting
    return render_template('professional-summary.html')


#CUSTOMER ROUTES

@app.route('/customer-home',methods=["GET","POST"])
def customer_home():
    # if request.method=="POST":
        #do someting
    return render_template('customer-home.html')

@app.route('/customer-search',methods=["GET","POST"])
def customer_search():
    # if request.method=="POST":
        #do someting
    return render_template('customer-search.html')

@app.route('/customer-summary',methods=["GET","POST"])
def customer_summary():
    # if request.method=="POST":
        #do someting
    return render_template('customer-summary.html')