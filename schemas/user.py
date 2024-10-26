from flask_marshmallow import Marshmallow
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import Schema, fields

from schemas.task import TaskSchema
from models.user import User


ma = Marshmallow()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "tasks",
        ]

    tasks = fields.Nested(TaskSchema(), many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserRequestSchema(Schema):
    username = fields.String(required=True, description="Unique identifier of user")
    email = fields.Email(required=True, description="Email address of user")
    password = fields.String(required=True, description="Password of user")
