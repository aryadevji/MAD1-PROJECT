from flask import render_template, current_app as app, request, session
from .models import *
from .auth import auth_requ



# professional search page
@app.route('/professional-search',methods=["GET","POST"])
@auth_requ
def professional_search():
    return render_template('professional-search.html')


#professional search results

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