
from flask import render_template, current_app as app, request, flash, redirect,send_file, session
from sqlalchemy import func
from .models import *
from .auth import auth_requ, admin_requ

# ADMIN ROUTES

@app.route('/admin-home',methods=["GET","POST"])
@admin_requ
def admin_home():
    services=Services.query.all()
    professionals=Professional.query.all()
    requests=Requests.query.all()

    return render_template('admin-home.html',services=services,professionals=professionals,requests=requests)


@app.route('/admin-search',methods=["GET","POST"])
@admin_requ
def admin_search():
        return render_template('admin-search.html')



@app.route('/admin-search-results', methods=["GET"])
@admin_requ
def admin_search_results():
    query = request.args.get('query')
    parameter = request.args.get('parameter')

    all_requests = []
    all_customers = []
    all_professionals = []

    if parameter == 'request':
        if query:
            # Join with the Services table and filter by service name
            requests = Requests.query.join(Services, Requests.service_id == Services.id) \
                                     .filter(Services.name.ilike(f"%{query}%")).all()
            all_requests.extend(requests)
        else:
            requests = Requests.query.all()
            all_requests.extend(requests)


    elif parameter == 'customer':
        if query:
            customers = Customer.query.filter(Customer.name.ilike(f"%{query}%")).all()
            all_customers.extend(customers)
        else:
            customers = Customer.query.all()
            all_customers.extend(customers)

    elif parameter == "professional":
        if query:
            professionals = Professional.query.filter(Professional.name.ilike(f"%{query}%")).all()
            all_professionals.extend(professionals)
        else:
            professionals = Professional.query.all()
            all_professionals.extend(professionals)

    return render_template('admin-search.html', all_professionals=all_professionals, all_customers=all_customers, all_requests=all_requests)







#Unblock professional
@app.route('/unblock-professional/<int:id>',methods=["POST"])
@admin_requ
def unblock_professional(id):
    professional = Professional.query.get(id)
    #changing active status
    professional.isactive=1
    db.session.commit()

    flash("Professional Unblocked !")
    return redirect('/admin-search')

#Block professional
@app.route('/block-professional/<int:id>',methods=["POST"])
@admin_requ
def block_professional(id):
    professional = Professional.query.get(id)
    #changing active status
    professional.isactive=3
    db.session.commit()

    flash("Professional Blocked !")
    return redirect('/admin-search')



#Unblock customer
@app.route('/unblock-customer/<int:id>',methods=["POST"])
@admin_requ
def unblock_customer(id):
    customer = Customer.query.get(id)
    #changing active status
    customer.isactive=1
    db.session.commit()

    flash("Customer Unblocked !")
    return redirect('/admin-search')

#Block customer
@app.route('/block-customer/<int:id>',methods=["POST"])
@admin_requ
def block_customer(id):
    customer = Customer.query.get(id)
    #changing active status
    customer.isactive=0
    db.session.commit()

    flash("Customer Blocked !")
    return redirect('/admin-search')








@app.route('/admin-summary',methods=["GET","POST"])
@admin_requ
def admin_summary():
        return render_template('admin-summary.html')


#ADDING NEW SERVICE

@app.route('/add-service',methods=["POST"])
@admin_requ
def add_service():
        S_name=request.form.get('service_name')
        B_price=request.form.get('base_price')
        S_description=request.form.get('description')
        
        if not S_name or not B_price or not S_description:
              flash("Please Fillout All the fields!",category="Failed")
              return redirect('/admin-home')
        
        existing_service= Services.query.filter((func.lower(Services.name) == func.lower(S_name))).first()

        if not existing_service:
            newService= Services(
                name=S_name,
                baseprice=B_price,
                description=S_description
            )
            db.session.add(newService)
            db.session.commit()
            flash("New Service Added!")
            return redirect('/admin-home')
        else:
            flash("Service Already Exists!", category="Failed")
            return redirect('/admin-home')
                

#EDITING EXISTING SERVICE

@app.route('/edit-service/<int:id>',methods=["POST"])
@admin_requ
def edit_service(id):
    
    service = Services.query.get(id)
    new_name=request.form.get('service_name')
    new_baseprice=int(request.form.get('base_price'))
    new_description=request.form.get('description')

    if not new_name or not new_baseprice or not new_description:
          flash("Fields can't be null !", category="Failed")
          return redirect('/admin-home')

    existing_service= Services.query.filter((func.lower(Services.name) == func.lower(new_name))).first()

    if not existing_service or existing_service.id == service.id:
            
            service.name= new_name
            service.baseprice= new_baseprice
            service.description= new_description
            db.session.commit()

            flash("Service Edited!")
            return redirect('/admin-home')
    else:
        flash("Service Already Exists !", category="Failed")
        
    return redirect('/admin-home')
                
   

#DELETING EXISTING SERVICE

@app.route('/delete-service/<int:id>', methods=["POST"])
@admin_requ
def delete_service(id):
    service = Services.query.get(id)
    # deleting the service from the database
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted !")
    
    return redirect('/admin-home')


#PROFESSIONALS REQUESTS
#Viewing the PDF file uploaded by the professional

@app.route('/view-pdf/<int:id>', methods=['GET',"POST"])
@admin_requ
def view_pdf(id):
    professional = Professional.query.get(id)

    if not professional or not professional.attachment:
        flash("No PDF found for this professional", category="Failed")
        return redirect('/admin-home')
    
    try:
        return send_file(professional.attachment, as_attachment=False)
    except Exception as e:
        flash(f"Error viewing PDF file : {str(e)}", category="Failed")
        return redirect('/admin-home')


#Accepting Request
@app.route('/accept-professional/<int:id>',methods=["POST"])
@admin_requ
def accept_professional(id):
    professional = Professional.query.get(id)
    #changing active status
    professional.isactive=1
    db.session.commit()

    flash("Professional Request Accepted!")
    return redirect('/admin-home')

#Declining Request
@app.route('/reject-professional/<int:id>',methods=["POST"])
@admin_requ
def reject_professional(id):
    professional = Professional.query.get(id)
    #changing active status
    professional.isactive=2
    db.session.commit()

    flash("Professional Request Rejected!")
    return redirect('/admin-home')


#Delete Request/Professional
#deletion from database
@app.route('/delete-professional/<int:id>',methods=["POST"])
@admin_requ
def delete_professional(id):
    professional = Professional.query.get(id)
    user= Users.query.get(professional.user_id)

    #from professional table
    db.session.delete(professional)
    #from user table
    db.session.delete(user)
    db.session.commit()

    flash("Service Professional Deleted !")
    return redirect('/admin-home')