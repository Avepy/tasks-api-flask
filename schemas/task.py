from flask_marshmallow import Marshmallow
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.task import Task
from marshmallow import Schema, fields

ma = Marshmallow()


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "time_spent",
            "date_started_at",
            "date_created",
            "date_modified",
            "date_deleted",
            "user_id",
        ]


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class TaskRequestSchema(Schema):
    title = fields.String(required=True, description="Title of the task")
    description = fields.String(description="Optional description of the task")


class TaskStatusUpdateSchema(Schema):
    task_id = fields.Integer(required=True, description="ID of the task")
    new_status = fields.Integer(required=True, description="New status for the task (1=OPEN, 2=PENDING, 3=COMPLETED)")


class TaskAssigneeUpdateSchema(Schema):
    user_id = fields.Integer(required=True, description="ID of the user to assign the task to")


class TaskReportSchema(Schema):
    task_id = fields.Integer()
    tile = fields.String()
    time_spent = fields.String()
    user_id = fields.Integer(allow_none=True)
    username = fields.String(allow_none=True)
    status = fields.String()

