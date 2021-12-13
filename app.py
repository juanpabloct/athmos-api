from re import M
from flask import Flask, request
from flask_migrate import Migrate

from database import db, ma
from models import Course, CourseSchema, User, UserSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

# cors


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/courses")
def courses():
    courses = Course.query.all()
    course_schema = CourseSchema(many=True)
    return course_schema.jsonify(courses)

# create a new course


@app.route("/courses", methods=["POST"])
def create_course():
    print(request.json)
    name = request.json['name']
    description = request.json['description']
    user_id = request.json['user_id']
    course = Course(name=name, description=description, user_id=user_id)
    db.session.add(course)
    db.session.commit()
    return "Course created", 201


@app.route('/users')
def users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.jsonify(users)


@app.route('/users/<int:user_id>')
def user(user_id):
    user = User.query.get(user_id)
    user_schema = UserSchema()
    return user_schema.jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return "User created", 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    username = request.json['username']
    email = request.json['email']
    user.username = username
    user.email = email
    db.session.commit()
    return "User updated", 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    db.session.delete(user)
    db.session.commit()
    return "User deleted", 200


@app.route('/users/<int:user_id>/courses')
def user_courses(user_id):
    courses = Course.query.where(Course.user_id == user_id)
    course_schema = CourseSchema(many=True)
    return course_schema.jsonify(courses)


@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return "Course not found", 404
    db.session.delete(course)
    db.session.commit()
    return "Course deleted", 200
