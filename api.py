from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from dotenv import load_dotenv
import os
from waitress import serve

# load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"


user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")
user_args.add_argument(
    "phone", type=str, required=True, help="Phone number cannot be blank"
)

# defining a schema for the response
userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "phone": fields.String,
}


class Users(Resource):
    @marshal_with(userFields)  # Apply the schema
    def get(self):
        users = UserModel.query.all()  # users data will be serialized
        return users

    @marshal_with(userFields)
    def post(self):
        # automatically send back a response if something is wrong
        args = user_args.parse_args()

        # Check if the email and phone already exists
        if UserModel.query.filter_by(email=args["email"]).first():
            abort(409, message="A user with this email already exists")

        elif UserModel.query.filter_by(phone=args["phone"]).first():
            abort(409, message="A user with this phone already exists")

        elif UserModel.query.filter_by(name=args["name"]).first():
            abort(409, message="A user with this name already exists")

        user = UserModel(name=args["name"], email=args["email"], phone=args["phone"])
        db.session.add(user)
        db.session.commit()

        user = UserModel.query.filter_by(id=user.id).first()
        return user, 201

        # users = UserModel.query.all()
        # return users, 201  # marshal_with handling serializing - no need to jsonify


class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with this id {id} cannot be found.")
        return user

    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()

        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with this id {id} cannot be found.")

        user.name = args["name"]
        user.email = args["email"]
        user.phone = args["phone"]
        db.session.commit()
        return user

    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with this id {id} cannot be found.")

        # UserModel.query.filter_by(id=id).delete()
        db.session.delete(user)
        db.session.commit()
        # return jsonify({"message": f"User with id {id} has been successfully deleted."}), 200

        users = UserModel.query.all()
        return users, 200


# endpoints
api.add_resource(Users, "/api/users/")
api.add_resource(User, "/api/users/<int:id>")


# endpoints
@app.route("/")
def index():
    return "<h1>Flask Simple CRUD REST API</h1>"


if __name__ == "__main__":
    # app.run( host="0.0.0.0", debug=True, port=8000)
    serve(app, host="0.0.0.0", port=8000)
