from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort


app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    ph_number = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"


user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")
user_args.add_argument(
    "phone", type=int, required=True, help="Phone number cannot be blank"
)

# defining a schema for the response
userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "phone": fields.Integer,
}


# endpoints
class Users(Resource):
    @marshal_with(userFields)  # Apply the schema
    def get(self):
        users = UserModel.query.all()  # users data will be serialized
        return users

    @marshal_with(userFields)
    def post(self):
        # automatically send back a response if something is wrong
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"], phone=args["phone"])
        db.session.add(user)
        db.session.commit()

        users = UserModel.query.all()
        return users, 201  # marshal_with handling serializing - no need to jsonify


api.add_resource(Users, "/api/users/")


# endpoints
@app.route("/")
def index():
    return "<h1>Hello World</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)
