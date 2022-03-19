from . import db
from werkzeug.security import generate_password_hash

class Property(db.Model):
    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    propertytitle = db.Column(db.String)
    numberofrooms = db.Column(db.Integer)
    numberofbathrooms = db.Column(db.Integer)
    location = db.Column(db.String)
    price = db.Column(db.Float)
    description  = db.Column(db.String)
    Type = db.Column(db.String)
    photo=  db.Column(db.String)
   


    def __init__(self,propertytitle,numberofrooms,numberofbathrooms,location, price, description, Type,photo ):
        self.propertytitle = propertytitle
        self.numberofrooms = numberofrooms
        self.numberofbathrooms = numberofbathrooms
        self.location = location
        self.price= price
        self.description = description
        self.Type = Type
        self.photo = photo
