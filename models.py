
from flask_login import UserMixin
from extensions import db 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')  # Role-based access (admin/user)

    def __repr__(self):
        return f"<User {self.username}>"