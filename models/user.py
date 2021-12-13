# User model with courses

from database import db, ma


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80))
    courses = db.relationship(
        'Course', back_populates='user',
    )

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'courses': [course.serialize() for course in self.courses]
        }

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')