from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy() #instance of SQLAlchemy

class Users(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    passhash=db.Column(db.String(256),nullable=False)
    role=db.Column(db.Integer,nullable=False)
    professionals = db.relationship('Professional', backref='user', lazy=True)
    customers = db.relationship('Customer', backref='user', lazy=True)


class Professional(db.Model):
    __tablename__="professional"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(300),nullable=False)
    service=db.Column(db.String(50),nullable=False)
    experience=db.Column(db.Integer,nullable=False)
    attachment=db.Column(db.String(300),nullable=True)
    isactive=db.Column(db.Integer,nullable=False,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Services(db.Model):
    __tablename__="services"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False,unique=True)
    baseprice=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    # professional_id=db.Column(db.S) fk
    


class Customer(db.Model):
    __tablename__="customer"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(300),nullable=False)
    isactive=db.Column(db.Boolean,nullable=False,default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



class Requests(db.Model):
    __tablename__="requests"
    id=db.Column(db.Integer,primary_key=True)
    # Customer_id=db.Column(db.String(50),unique=True,nullable=False) fk
    request_date = db.Column(db.Date,nullable=False,default=db.func.current_date())
    # service_id=db.Column(db.String,nullable=False) fk
    date_complition=db.Column(db.Date)


class Transactions(db.Model):
    __tablename__="transactions"
    id=db.Column(db.Integer,primary_key=True)
    # user_id=db.Column(db.String(50),unique=True,nullable=False) fk

