from flask import render_template, current_app as app, request, flash, redirect, session
from .models import *
from .auth import auth_requ

# PROFESSIONAL ROUTES

@app.route('/professional-home', methods=["GET", "POST"])
@auth_requ
def professional_home():
    user_det = Users.query.get(session.get('user_id'))
    pro_det = Professional.query.filter_by(user_id=session['user_id']).first()
    req_det = Requests.query.filter_by(professional_id=pro_det.id).all()
    reviews= Reviews.query.filter_by(professional_id=pro_det.id).all()

    return render_template('professional-home.html', user=user_det, professional=pro_det, requests=req_det,reviews=reviews)


#closing active service from professionals side
@app.route('/close-request/<int:id>', methods=['POST'])
@auth_requ
def close_request(id):
    from sqlalchemy import func
    service_request = Requests.query.get(id)
    
    service_request.status = 3
    service_request.date_complition = func.current_date()
    db.session.commit()

    flash("Service closed !")
    return redirect('/professional-home')






# Accepting Request
@app.route('/accept-service/<int:id>', methods=["POST"])
@auth_requ
def accept_service(id):
    # Fetch the request by its id
    request = Requests.query.get(id)

    # Change status to 'Accepted'
    request.status = 1
    db.session.commit()

    flash("Service Request Accepted!")
    return redirect('/professional-home')


# Declining Request
@app.route('/reject-service/<int:id>', methods=["POST"])
@auth_requ
def reject_service(id):
    # Fetch the request by its id
    request = Requests.query.get(id)

    # Change status to 'Rejected'
    request.status = 2
    db.session.commit()

    flash("Service Request Rejected!")
    return redirect('/professional-home')



@app.route('/professional-search',methods=["GET","POST"])
@auth_requ
def professional_search():
    return render_template('professional-search.html')



@app.route('/professional-search-results', methods=['GET'])
@auth_requ
def professional_search_results():
    pro_det = Professional.query.filter_by(user_id=session['user_id']).first()
    query = request.args.get('query')
    parameter = request.args.get('parameter')

    results = []

    if parameter == 'date':
        if query:
            requests = Requests.query.filter(Requests.request_date == query, Requests.professional_id == pro_det.id).all()
        else:
            requests = Requests.query.all()
        for service_request in requests:
            customer = Customer.query.get(service_request.customer_id)
            review = Reviews.query.filter_by(request_id=service_request.id).first()
            results.append((service_request, customer, review))

    elif parameter == 'pincode':

        if query:
            customers = Customer.query.filter(Customer.pincode == int(query)).all()
        else:
            customers =Customer.query.all()
        for customer in customers:
            requests = Requests.query.filter_by(customer_id=customer.id, professional_id=pro_det.id).all()
            for service_request in requests:
                review = Reviews.query.filter_by(request_id=service_request.id).first()
                results.append((service_request, customer, review))

    elif parameter == 'rating':

        if query:
            reviews = Reviews.query.filter(Reviews.rating == int(query)).all()
        else:
            reviews =Reviews.query.all()

        for review in reviews:
            service_request = Requests.query.filter_by(id=review.request_id, professional_id=pro_det.id).first()
            if service_request:
                customer = Customer.query.get(service_request.customer_id)
                results.append((service_request, customer, review))

    return render_template('professional-search.html', results=results)





@app.route('/professional-summary',methods=["GET","POST"])
@auth_requ
def professional_summary():
        return render_template('professional-summary.html')



# Edit Profiles
# For Professionals

@app.route('/edit-professional-profile', methods=['POST'])
@auth_requ
def edit_professional_profile():
    new_name=request.form.get('name')
    new_username=request.form.get('username')
    new_email=request.form.get('email')
    new_address=request.form.get('address')
    new_pincode=int(request.form.get('pincode'))
    new_experience=int(request.form.get('experience'))


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
    if new_name and new_name != pro_det.name:
        pro_det.name = new_name
        updated= True
        flash("Name Update Success!")
    

    if new_email and new_email != pro_det.email:
        pro_det.email = new_email
        updated= True
        flash("Email Update Success!")

    if new_username and new_username != user_det.username:
        user_det.username = new_username
        updated= True
        flash("Username Update Success!")

    if new_address and new_address != pro_det.address:
        pro_det.address = new_address
        updated = True
        flash("Address Update Success!")


    if new_pincode and new_pincode > 0 and new_pincode != pro_det.pincode:
        pro_det.pincode = new_pincode
        updated = True
        flash("Pincode Update Success!")

    if new_experience and new_experience > 0 and new_experience != pro_det.experience:
        pro_det.experience = new_experience
        updated = True
        flash("Experience Update Success!")


    if updated:
        db.session.commit()
    else:
        flash("No field Updated!", category="Failed")
    return redirect('/professional-home')
    