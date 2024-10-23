
from flask import render_template, current_app as app, request, flash, redirect
from .models import *
from .auth import  admin_requ




#Search Page

@app.route('/admin-search',methods=["GET","POST"])
@admin_requ
def admin_search():
        return render_template('admin-search.html')


#Search Results

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