from flask import render_template, current_app as app, request, flash, redirect, session
from  functools import wraps
import os
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


# DEFINING DECORATERs
#auth required decorater
def auth_requ(funct):
    @wraps(funct)
    def inner_funct(*args ,**kwargs):
        if session.get('user_id'):
            return funct(*args,**kwargs)
        else:
            flash("Please Login to Continue!", category="Failed")
            return redirect('/login')
    return inner_funct

#admin auth required decorater
def admin_requ(funct):
    @wraps(funct)
    def inner_funct(*args ,**kwargs):
        if 'user_id' not in session:
            flash("Please Login to Continue!", category="Failed")
            return redirect('/login')
        
        user= Users.query.get(session['user_id'])
        if user.role == 0:
            return funct(*args,**kwargs)
        if user.role == 1:
            flash("You are not authorized to access this page", category="Failed")
            return redirect('/customer-home')
        if user.role == 2:
            flash("You are not authorized to access this page", category="Failed")
            return redirect('/professional-home')
        
    return inner_funct


#register  or choose page
@app.route('/register')
def register():
    return render_template('register.html')



# CUSTOMERS REGISTERATION 

@app.route('/register-customer',methods=["GET","POST"])
def register_customer():
    if request.method == "POST":

        
        try:
            full_name = request.form.get("customername")
            cust_email = request.form.get("customeremail")
            user_name = request.form.get("customerusername")
            password = request.form.get("customerpassword")
            cust_add = request.form.get("customeraddress")
            cust_pincode = request.form.get("customerpincode")

            # for database intergrity check username or email already exists
            existing_user = Users.query.filter((Users.username == user_name)).first()
            existing_email=Customer.query.filter((Customer.email == cust_email)).first()

            if existing_user or existing_email:
                flash("User already exists. Please use a different username or email address !", category="Failed")
                return redirect("/register-customer")

            cust_user = Users(
                username=user_name,
                passhash=generate_password_hash(password, method='pbkdf2:sha256'),
                role=1
            )

            db.session.add(cust_user)
            db.session.flush() 

            new_customer = Customer(
                name=full_name,
                email=cust_email,
                pincode=cust_pincode,
                address=cust_add,
                user_id=cust_user.id
            )

            db.session.add(new_customer)
            db.session.commit()

            # Registration success, redirect to login page with success message
            flash("Registration successful!", category="Success")
            return render_template("login.html")

        except Exception as e:
            db.session.rollback()  # Rollingback  the changes, if something goes wrong
            flash(f"Registration failed: {str(e)}", category="Failed")
            return render_template('register-customer.html')  #  Back to Registration


    return render_template('register-customer.html')



# PROFESSIONAL REGISTERATION

@app.route('/register-professional', methods=["GET", "POST"])
def register_professional():
    services=Services.query.all()
    if request.method == "POST":

        try:
            full_name = request.form.get("profname")
            prof_email = request.form.get("profemail")
            user_name = request.form.get("profusername")
            password = request.form.get("profpassword")
            service_name = request.form.get("servicename")
            prof_experience = request.form.get("experience")
            prof_add = request.form.get("profadd")
            prof_pincode = request.form.get("profpincode")

            # for database intergrity check username or email already exists
            existing_user = Users.query.filter((Users.username == user_name)).first()
            existing_email=Professional.query.filter((Professional.email == prof_email)).first()

            if existing_user or existing_email:
                flash("User already exists. Please use a different username or email address !", category="Failed")
                return redirect("/register-professional")

            # Checking if a file is uploaded or not

            if 'file' not in request.files:
                flash("No file uploaded", category="Failed")
                return redirect(request.url)

            file = request.files['file']

            # If the user does not select a file, browser submits an empty part without a filename
            if file.filename == '':
                flash("No file selected", category="Failed")
                return redirect(request.url)

            # Directly check the file extension
            if not file.filename.endswith('.pdf'):
                flash("Invalid file type. Please upload a PDF.", category="Failed")
                return redirect(request.url)

                        # Create the user object first
            prof_user = Users(
                username=user_name,
                passhash=generate_password_hash(password, method='pbkdf2:sha256'),
                role=2 
            )
            db.session.add(prof_user)
            db.session.flush()  # Flush to get the ID before committing

            # Now, create the professional object
            new_professional = Professional(
                name=full_name,
                email=prof_email,
                pincode=prof_pincode,
                address=prof_add,
                service=service_name,
                experience=prof_experience,
                user_id=prof_user.id  # Use the flushed ID from prof_user
            )

            db.session.add(new_professional)
            db.session.flush()  # Flush to get the professional ID

            # Save the file with a unique name
            professional_id = new_professional.id
            filename = f"pro_{professional_id}_{secure_filename(file.filename)}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_professional.attachment = file_path  # Assign the saved file path

            db.session.commit()  # Commiting all changes

            # Registration success, redirect to login page with success message
            flash("Registration successful!", category="Success")
            return render_template("login.html")

        except Exception as e:
            db.session.rollback()  # Rollingback  the changes, if something goes wrong
            flash(f"Registration failed: {str(e)}", category="Failed")
            return render_template('register-professional.html')  #  Back to Registration

    return render_template('register-professional.html',services=services)


#LOGIN USERS

@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = request.form.get("loginusername")
        password = request.form.get("loginpassword")
        urole = request.form.get("loginrole")

        if not user_name or not password or not urole:
            flash("Please fill out all fields", category="Failed")
            return render_template('login.html')

        # Fetch user by username and role
        usr = Users.query.filter_by(username=user_name, role=urole).first()

        if usr is None:
            flash("User does not exist", category="Failed")
            return render_template('login.html')

        # Check if password matches
        if not check_password_hash(usr.passhash, password):
            flash("Invalid Password", category="Failed")
            return render_template('login.html')

        # Set session
        session['user_id'] = usr.id

        # Redirect based on user role, but first check if account is active
        if usr.role == 0:
            flash("Login Success!")
            return redirect("/admin-home")
        
        elif usr.role == 1:
            customer = Customer.query.filter_by(user_id=usr.id).first()
            if customer.isactive != 1:
                flash("Your Customer account is disabled !", category="Failed")
                return render_template('login.html')
            flash("Login Success!")
            return redirect('/customer-home')
        
        elif usr.role == 2:
            professional = Professional.query.filter_by(user_id=usr.id).first()
            if professional.isactive != 1:
                flash("Your Professional account is disabled or not activated yet!", category="Failed")
                return render_template('login.html')
            flash("Login Success!")
            return redirect('/professional-home')

    return render_template('login.html')



#LOGOUT USER

@app.route('/logout', methods=['POST'])
@auth_requ
def logout():
    session.clear()
    flash("You are Logged Out", category="Success")
    return redirect('/login')