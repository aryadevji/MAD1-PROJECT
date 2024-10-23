from flask import render_template, current_app as app, session
from .models import Requests,Professional,Reviews
from .auth import auth_requ


# professional summary page
@app.route('/professional-summary',methods=["GET","POST"])
@auth_requ
def professional_summary():
    pro_det = Professional.query.filter_by(user_id=session['user_id']).first()
    professional_id = pro_det.id
    
    #c1
    ratings = Reviews.query.filter_by(professional_id=professional_id).all()
    rating_counts = [0] * 5
    for review in ratings:
        rating_counts[review.rating - 1] += 1

    #c2
    total_requests = Requests.query.filter_by(professional_id=professional_id).count()
    total_pending = Requests.query.filter_by(professional_id=professional_id, status=0).count()
    total_accepted = Requests.query.filter_by(professional_id=professional_id, status=1).count()  
    total_closed = Requests.query.filter_by(professional_id=professional_id, status=3).count()  
    total_rejected = Requests.query.filter_by(professional_id=professional_id, status=2).count()

    return render_template('professional-summary.html', 
                           rating_counts=rating_counts, 
                           total_requests=total_requests,
                           total_accepted=total_accepted,
                           total_closed=total_closed,
                           total_rejected=total_rejected,
                           total_pending=total_pending)