# course model associated to user
from database import db, ma


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='courses')

    def __repr__(self):
        return '<Course %r>' % self.name


class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'user_id')