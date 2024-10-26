from flask import abort
from flask_apispec import MethodResource, doc, marshal_with, use_kwargs

from controllers.user_controller import create_user, get_all_users, get_user_by_id, delete_user
from schemas.user import UserSchema, UserRequestSchema


class UserResource(MethodResource):
    @doc(description="Creates a new user", tags=["User"])
    @use_kwargs(UserRequestSchema, location="json")
    @marshal_with(UserSchema, code=201)
    def post(self, **kwargs):
        new_user = create_user(kwargs.get("username"), kwargs.get("email"), kwargs.get("password"))

        if not new_user:
            abort(400, description="There was an error creating the user. Please try again.")

        return new_user, 201

    @doc(description="Get all users", tags=["User"])
    @marshal_with(UserSchema(many=True))
    def get(self):
        users = get_all_users()
        return users


class UserDetailResource(MethodResource):
    @doc(description="Get user by ID", tags=["User"])
    @marshal_with(UserSchema)
    def get(self, user_id):
        user = get_user_by_id(user_id)

        if not user:
            abort(404, description="User not found.")

        return user


    @doc(description="Delete user by ID", tags=["User"])
    @marshal_with(UserSchema)
    def delete(self, user_id):
        user = delete_user(user_id)

        if not user:
            abort(404, description="User not found.")

        return user, 200

