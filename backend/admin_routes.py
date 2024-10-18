
from flask import render_template, current_app as app, request, flash, redirect, session
from .models import *
from .auth import auth_requ

# ADMIN ROUTES

@app.route('/admin-home',methods=["GET","POST"])
@auth_requ
def admin_home():
    return render_template('admin-home.html')



@app.route('/admin-search',methods=["GET","POST"])
@auth_requ
def admin_search():
        return render_template('admin-search.html')


@app.route('/admin-summary',methods=["GET","POST"])
@auth_requ
def admin_summary():
        return render_template('admin-summary.html')



@app.route('/add-service',methods=["POST"])
@auth_requ
def add_service():
       return "service added"