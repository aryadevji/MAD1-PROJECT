from flask import render_template, current_app as app, request, flash, redirect, session
from .models import *
from .auth import auth_requ


#Customer Homepage

@app.route('/customer-home',methods=["GET","POST"])
@auth_requ
def customer_home():
    user_det = Users.query.get(session.get('user_id'))
    cust_det = Customer.query.filter_by(user_id=session['user_id']).first()
    service_requests= Requests.query.filter_by(customer_id=cust_det.id).all()
    return render_template('customer-home.html',user=user_det, customer=cust_det,service_requests=service_requests)



# Edit customer Profile

@app.route('/edit-customer-profile', methods=['POST'])
@auth_requ
def edit_customer_profile():
    new_name=request.form.get('name')
    new_username=request.form.get('username')
    new_email=request.form.get('email')
    new_address=request.form.get('address')
    new_pincode=int(request.form.get('pincode'))

    user_det = Users.query.get(session.get('user_id'))
    cust_det = Customer.query.filter_by(user_id=session['user_id']).first()
         
    # Check for existing username and email
    if new_username and new_username != user_det.username:
        existing_username = Users.query.filter_by(username=new_username).first()
        if existing_username:
            flash("Username Already Exists!", category="Failed")
            return redirect('/customer-home') 

    if new_email and new_email != cust_det.email:
        existing_email = Customer.query.filter_by(email=new_email).first()
        if existing_email:
            flash("Email Already Exists!", category="Failed")
            return redirect('/customer-home')

    # Updated profile fields
    updated= False
    if new_name and new_name != cust_det.name:
        cust_det.name = new_name
        updated= True
        flash("Name Update Success!")

    if new_email and new_email != cust_det.email:
        cust_det.email = new_email
        updated= True
        flash("Email Update Success!")

    if new_username and new_username != user_det.username:
        user_det.username = new_username
        updated= True
        flash("Username Update Success!")

    if new_address and new_address != cust_det.address:
        cust_det.address = new_address
        updated = True
        flash("Address Update Success!")

    if new_pincode and new_pincode > 0 and new_pincode != cust_det.pincode:
        cust_det.pincode = new_pincode
        updated = True
        flash("Pincode Update Success!")

    # Commit changes if any field was updated
    if updated:
        db.session.commit()
    else:
        flash("No field Updated!", category="Failed")

    return redirect('/customer-home') 



#Closing an Active Service and submitting Review and Rating for that

@app.route('/close-service-request/<int:request_id>', methods=['POST'])
@auth_requ
def close_service(request_id):
    from sqlalchemy import func
    service_request = Requests.query.get(request_id)
    
    service_request.status = 3
    service_request.date_complition = func.current_date()
    db.session.commit()

    review_message = request.form.get('review')
    rating = int(request.form.get('rating'))

    review = Reviews(
        review=review_message,
        rating=rating,
        customer_id=service_request.customer_id,
        professional_id=service_request.professional_id,
        service_id=service_request.service_id,
        request_id=request_id
    )

    db.session.add(review)
    db.session.commit()

    flash("Service closed, thanks for your feedback !")
    return redirect('/customer-home')


#Edit existing Service request

@app.route('/edit-service-req/<int:id>',methods=["POST"])
@auth_requ
def edit_service_req(id):
    from datetime import datetime
    update_date = request.form.get('req_date')
    resend = request.form.get('resend')
    edit_service_request = Requests.query.get(id)

    if update_date and resend and resend.isdigit():
        
        resend = int(resend)
        update_date = datetime.strptime(update_date, '%Y-%m-%d').date()
        edit_service_request.status = resend
        edit_service_request.request_date = update_date
        db.session.commit()
        if resend == 0:
            flash("Service Request Updated and Sent Back Again !")
        else:
            flash("Service Request Updated !")

    
    else:
        flash("Service Request not Updated fill all fields !", category="Failed")
           
    return redirect('/customer-home')
