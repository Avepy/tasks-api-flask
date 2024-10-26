from flask import Flask, url_for
from extensions import db, migrate
from flask_apispec import FlaskApiSpec
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config
from resources.task_resource import TaskResource, TaskDetailResource, TaskReportResource
from resources.user_resource import UserResource, UserDetailResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Swagger
    swagger_url = "/swagger"
    api_url = "/swagger.json"
    swagger_ui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, config={'app_name': "Task Management API"})
    app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)

    # Routes
    app.add_url_rule("/tasks", view_func=TaskResource.as_view("tasks"))
    app.add_url_rule("/tasks/<int:task_id>", view_func=TaskDetailResource.as_view("task_detail"))
    app.add_url_rule("/reports/tasks/time_spent", view_func=TaskReportResource.as_view("task_report"))
    app.add_url_rule("/users", view_func=UserResource.as_view("users"))
    app.add_url_rule("/users/<int:user_id>", view_func=UserDetailResource.as_view("user_detail"))

    # ApiSpec
    docs = FlaskApiSpec(app)
    docs.register(TaskResource, endpoint="tasks")
    docs.register(TaskDetailResource, endpoint="task_detail")
    docs.register(TaskReportResource, endpoint="task_report")
    docs.register(UserResource, endpoint="users")
    docs.register(UserDetailResource, endpoint="user_detail")


    @app.route('/swagger.json')
    def create_swagger_spec():
        return docs.spec.to_dict()

    with app.app_context():
        print(f"\033[94m\033[1m[DEBUG] Swagger UI available at: {url_for('swagger_ui.show')}", flush=True)

    return app


if __name__ == "__main__":
    app_builder = create_app()
    app_builder.run(debug=True)
