from flask import render_template, current_app as app, session
from .models import Customer, Requests
from .auth import auth_requ



@app.route('/customer-summary',methods=["GET","POST"])
@auth_requ
def customer_summary():
    cust_det = Customer.query.filter_by(user_id=session['user_id']).first()
    customer_id = cust_det.id

    # Example query to get counts for the requests
    closed_requests_count = Requests.query.filter_by(customer_id=customer_id, status=3).count()
    pending_requests_count = Requests.query.filter_by(customer_id=customer_id, status=0).count()
    
    active_requests_count = Requests.query.filter_by(customer_id=customer_id, status=1).count()

    labels = ['Closed Requests', 'Pending Requests', 'Active Requests']
    data = [closed_requests_count, pending_requests_count, active_requests_count]

    return render_template('customer-summary.html', labels=labels, data=data)