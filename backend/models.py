from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy() #instance of SQLAlchemy

class Users(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    passhash=db.Column(db.String(256),nullable=False)
    role=db.Column(db.Integer,nullable=False)

    #relationship with Professional and Customer
    professionals = db.relationship('Professional', backref='user', lazy=True)
    customers = db.relationship('Customer', backref='user', lazy=True)


class Professional(db.Model):
    __tablename__ = "professional"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    service=db.Column(db.String(50),nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    attachment = db.Column(db.String(300), nullable=True)
    isactive = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #relation to reviews model
    reviews=db.relationship('Reviews', backref='professional', lazy=True)
    # Relationship to Requests model
    requests = db.relationship('Requests', backref='professional', lazy=True)
    

class Services(db.Model):
    __tablename__ = "services"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    baseprice = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    #relationship to reviews model
    reviews=db.relationship('Reviews', backref='services', lazy=True)
    # Relationship to Requests model
    requests = db.relationship('Requests', backref='services', lazy=True)
    



class Customer(db.Model):
    __tablename__="customer"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(300),nullable=False)
    isactive=db.Column(db.Boolean,nullable=False,default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

     # Relationship to Requests model
    requests=db.relationship('Requests', backref='customer',lazy=True)
    #relationship to reviews model
    reviews=db.relationship('Reviews', backref='customer', lazy=True)



class Requests(db.Model):
    __tablename__="requests"
    id=db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    request_date = db.Column(db.Date,nullable=False,default=db.func.current_date())
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    status= db.Column(db.Integer, nullable=False, default=0)
    date_complition=db.Column(db.Date)

    #relation to reviews model
    reviews=db.relationship('Reviews', backref='requests', lazy=True)

    #relation to service model
    service = db.relationship('Services',backref='requests_services', lazy=True)




class Reviews(db.Model):
    __tablename__="reviews"
    id=db.Column(db.Integer,primary_key=True)
    review=db.Column(db.String(300),nullable=False)
    rating=db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)


