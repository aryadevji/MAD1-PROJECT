from flask import Flask,render_template, current_app as app, request, flash, redirect, session
from  functools import wraps
import os
from .models import *
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

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

    return render_template('register-professional.html')


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


#LOGIN USERS

@app.route('/')
@app.route('/login',methods=["GET","POST"])
def index():
    if request.method=="POST":
        user_name=request.form.get("loginusername")
        password=request.form.get("loginpassword")
        urole=int(request.form.get("loginrole"))

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
            
        session['user_id'] = usr.id
        flash("Login Success!", category="Success")

        if usr.role == 0:                                #login based on roles
            return render_template("admin-home.html")
        elif usr.role == 1:
            return redirect('/customer-home')
        elif usr.role == 2:
            return redirect('professional-home')
        
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


# PROFESSIONAL ROUTES

@app.route('/professional-home',methods=["GET","POST"])
@auth_requ
def professional_home():
    user_det = Users.query.get(session.get('user_id'))
    pro_det = Professional.query.filter_by(user_id=session['user_id']).first()
    return render_template('professional-home.html', user=user_det, professional=pro_det)


@app.route('/professional-search',methods=["GET","POST"])
@auth_requ
def professional_search():
        return render_template('professional-search.html')


@app.route('/professional-summary',methods=["GET","POST"])
@auth_requ
def professional_summary():
        return render_template('professional-summary.html')


#CUSTOMER ROUTES

@app.route('/customer-home',methods=["GET","POST"])
@auth_requ
def customer_home():
    user_det = Users.query.get(session.get('user_id'))
    cust_det = Customer.query.filter_by(user_id=session['user_id']).first()
    return render_template('customer-home.html',user=user_det, customer=cust_det)


@app.route('/customer-search',methods=["GET","POST"])
@auth_requ
def customer_search():
        return render_template('customer-search.html')


@app.route('/customer-summary',methods=["GET","POST"])
@auth_requ
def customer_summary():
        return render_template('customer-summary.html')
    


# Edit Profiles

# For Customers

@app.route('/edit-customer-profile', methods=['POST'])
@auth_requ
def edit_customer_profile():
    new_name=request.form.get('name')
    new_username=request.form.get('username')
    new_email=request.form.get('email')
    new_address=request.form.get('address')
    new_pincode=request.form.get('pincode')

    user_det = Users.query.get(session.get('user_id'))
    cust_det = Customer.query.filter_by(user_id=session['user_id']).first()

    # Check for existing username and email
    if new_username and new_username != user_det.username:
        existing_username = Users.query.filter_by(username=new_username).first()
        if existing_username:
            flash("Username Already Exists!", category="Failed")
            return redirect('/customer-home')  # Redirect to the appropriate page

    if new_email and new_email != cust_det.email:
        existing_email = Customer.query.filter_by(email=new_email).first()
        if existing_email:
            flash("Email Already Exists!", category="Failed")
            return redirect('/customer-home')  # Redirect to the appropriate page

    # Updated profile fields
    updated= False
    if new_name:
        cust_det.name = new_name
        updated= True
        flash("Name Update Success!")

    if new_email:
        cust_det.email = new_email
        updated= True
        flash("Email Update Success!")

    if new_username:
        user_det.username = new_username
        updated= True
        flash("Username Update Success!")

    if new_address:
        cust_det.address = new_address
        updated = True
        flash("Address Update Success!")

    if new_pincode:
        cust_det.pincode = new_pincode
        updated = True
        flash("Pincode Update Success!")

    # Commit changes if any field was updated
    if updated:
        db.session.commit()

    return redirect('/customer-home')  # Redirect after updating


# For Professionals

@app.route('/edit-professional-profile', methods=['POST'])
@auth_requ
def edit_professional_profile():
    new_name=request.form.get('name')
    new_username=request.form.get('username')
    new_email=request.form.get('email')
    new_address=request.form.get('address')
    new_pincode=request.form.get('pincode')


    user_det = Users.query.get(session.get('user_id'))
    pro_det = Professional.query.filter_by(user_id=session['user_id']).first()

    if new_username and new_username != user_det.username:
        existing_username = Users.query.filter_by(username=new_username).first()
        if existing_username:
            flash("Username Already Exists!", category="Failed")
            return redirect('/professional-home')

    if new_email and new_email != pro_det.email:
        existing_email = Customer.query.filter_by(email=new_email).first()
        if existing_email:
            flash("Email Already Exists!", category="Failed")
            return redirect('/customer-home') 

    updated= False
    if new_name:
        pro_det.name = new_name
        updated= True
        flash("Name Update Success!")

    if new_email:
        pro_det.email = new_email
        updated= True
        flash("Email Update Success!")

    if new_username:
        user_det.username = new_username
        updated= True
        flash("Username Update Success!")

    if new_address:
        pro_det.address = new_address
        updated = True
        flash("Address Update Success!")

    if new_pincode:
        pro_det.pincode = new_pincode
        updated = True
        flash("Pincode Update Success!")

    if updated:
        db.session.commit()
    return redirect('/professional-home')




#LOGOUT USER

@app.route('/logout', methods=['POST'])
@auth_requ
def logout():
    session.clear()
    flash("You are Logged Out", category="Success")
    return redirect('/login')