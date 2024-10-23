from flask import render_template, current_app as app, request, flash, redirect, session
from .models import *
from .auth import auth_requ



#Customer Search Page

@app.route('/customer-search',methods=["GET","POST"])
@auth_requ
def customer_search():
    return render_template('customer-search.html')


# Customer Search results

@app.route('/search-results', methods=['GET'])
@auth_requ
def search_results():
    query = request.args.get('query')
    parameter = request.args.get('parameter')

    service_professionals = []
    
    if parameter == 'service':
        # services based on the query
        if query:
            services = Services.query.filter(Services.name.ilike(f"%{query}%")).all()
        else:
            services =Services.query.all()
        
        for service in services:
            # professionals that match the service name
            professionals = Professional.query.filter(Professional.service == service.name).all()
            service_professionals.append((service, professionals))
            
    elif parameter == 'price':
        # services based on base price
        if query:
            services = Services.query.filter(Services.baseprice.ilike(f"%{query}%")).all()
        else:
            services =Services.query.all()
        
        for service in services:
            #professionals that match the service name
            professionals = Professional.query.filter(Professional.service == service.name).all()
            service_professionals.append((service, professionals))

    return render_template('customer-search.html', service_professionals=service_professionals)



#Booking any service

@app.route('/book-service/<int:service_id>/<int:professional_id>', methods=['POST'])
@auth_requ
def book_service(service_id, professional_id):
    customer = Customer.query.filter_by(user_id=session.get('user_id')).first()


    new_request = Requests(
        customer_id=customer.id,
        service_id=service_id,
        professional_id=professional_id
    )

    db.session.add(new_request)
    db.session.commit()

    flash('Service booked!', 'success')

    return redirect('/customer-search')