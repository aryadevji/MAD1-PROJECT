
from flask import render_template, current_app as app
from .models import Services,Professional,Requests
from .auth import  admin_requ



#Admin Summary

@app.route('/admin-summary',methods=["GET","POST"])
@admin_requ
def admin_summary():

    # Get requests per service
    services = Services.query.all()
    service_labels = [service.name for service in services]
    service_requests = [len(Requests.query.filter_by(service_id=service.id).all()) for service in services]

    # Get requests per professional
    professionals = Professional.query.all()
    professional_labels = [professional.name for professional in professionals]
    professional_requests = [len(Requests.query.filter_by(professional_id=professional.id).all()) for professional in professionals]

    return render_template('admin-summary.html',
                            service_labels=service_labels,
                            service_data=service_requests,
                            professional_labels=professional_labels,
                            professional_data=professional_requests)