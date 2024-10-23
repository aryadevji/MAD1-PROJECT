
from flask import render_template, current_app as app, request, flash, redirect,send_file
from sqlalchemy import func
from .models import *
from .auth import  admin_requ



#Home Page

@app.route('/admin-home',methods=["GET","POST"])
@admin_requ
def admin_home():
    services=Services.query.all()
    professionals=Professional.query.all()
    requests=Requests.query.all()

    return render_template('admin-home.html',services=services,professionals=professionals,requests=requests)



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


#Delete Professional-request
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