from flask import request, abort, Response
from flask_apispec import MethodResource, doc, marshal_with, use_kwargs

from enums.report_format_type import ReportFormatType
from enums.task_status import TaskStatus
from enums.order_type import OrderType

from schemas.task import TaskSchema, TaskRequestSchema, TaskStatusUpdateSchema, TaskAssigneeUpdateSchema, \
    TaskReportSchema
from controllers.task_controller import get_all_tasks, get_task_by_id, create_task, delete_task, update_task_status, \
    assign_task_to_user, get_task_time_spent_report, generate_task_time_spent_graph, generate_task_time_spent_pdf


class TaskResource(MethodResource):
    @doc(description="Get all tasks with optional filters and sorting",
         tags=["Task"],
         params={
             'status': {"description": "Filter tasks by status (1=OPEN, 2=PENDING, 3=COMPLETED)", "in": 'query', "type": "integer"},
             'sort_by': {"description": "Column to sort by (id, title, status, see more at Models -> Task)", "in": "query", "type": "string"},
             'order': {"description": "Sorting order (1=ASC or 2=DESC)", "in": "query", "type": "integer"},
         })
    @marshal_with(TaskSchema(many=True))
    def get(self):
        status_value = request.args.get("status", type=int)
        status = None
        if status_value is not None:
            try:
                status = TaskStatus(status_value)
            except ValueError:
                abort(400, description="Invalid status value provided. Must be 1 (OPEN), 2 (PENDING), or 3 (COMPLETED).")

        sort_by = request.args.get("sort_by", default="id")

        order_value = request.args.get("order", type=int)
        order = None
        if order_value is not None:
            try:
                order = OrderType(order_value)
            except ValueError:
                abort(400, description="Invalid order value provided. Must be 1 (ASC) or 2 (DESC).")

        tasks = get_all_tasks(status, sort_by, order)
        return tasks


    @doc(description="Create a new task", tags=["Task"])
    @use_kwargs(TaskRequestSchema, location="json")
    @marshal_with(TaskSchema, code=201)
    def post(self, **kwargs):
        new_task = create_task(kwargs.get("title"), kwargs.get("description", ""))

        if not new_task:
            abort(400, description="There was an error creating the task. Please try again.")

        return new_task, 201


    @doc(description="Change task status by its ID", tags=["Task"])
    @use_kwargs(TaskStatusUpdateSchema, location="json")
    @marshal_with(TaskSchema)
    def patch(self, **kwargs):
        task_id = kwargs.get("task_id")

        if task_id < 0:
            abort(400, description="Task ID must be greater than 0.")

        new_status_value = kwargs.get("new_status")
        task, status_code = update_task_status(task_id, new_status_value)

        if not task:
            abort(status_code, description="Invalid task or status update.")

        return task


class TaskDetailResource(MethodResource):
    @doc(description="Get a task by ID", tags=["Task"])
    @marshal_with(TaskSchema)
    def get(self, task_id):
        task = get_task_by_id(task_id)

        if not task:
            return abort(404, description="Task not found.")

        return task


    @doc(description="Delete a task by ID", tags=["Task"])
    @marshal_with(TaskSchema)
    def delete(self, task_id):
        task = delete_task(task_id)

        if not task:
            return abort(404, description="Task not found.")

        return task, 200


    @doc(description="Assign a task to a user", tags=["Task"])
    @use_kwargs(TaskAssigneeUpdateSchema, location="json")
    @marshal_with(TaskSchema)
    def patch(self, task_id, **kwargs):
        user_id = kwargs.get("user_id")

        if user_id < 0:
            return abort(400, description="User ID must be greater than 0.")

        task, status_code = assign_task_to_user(task_id, user_id)

        if not task:
            return abort(status_code, description="Task or user not found.")

        return task, 200


class TaskReportResource(MethodResource):
    @doc(description="Get a report of time spent on every task",
         tags=["Reports"],
         params={
            "report_format": {
                "description": "Format of the report (1=JSON, 2=GRAPH, 3=PDF)",
                "in": "query",
                "type": "integer",
                "required": True
            }
         })
    @marshal_with(TaskReportSchema(many=True))
    def get(self):
        report_format_value = request.args.get("report_format", type=int)

        report_format = None

        try:
            print(report_format_value)
            report_format = ReportFormatType(report_format_value)
        except ValueError:
            abort(400, description="Invalid status value provided. Must be 1=JSON or 2=GRAPH or 3=PDF.")

        result = None, 400

        if report_format == ReportFormatType.JSON:
            result = get_task_time_spent_report()
        elif report_format == ReportFormatType.GRAPH:
            image_data = generate_task_time_spent_graph()
            result = Response(image_data, mimetype="image/png")
        elif report_format == ReportFormatType.PDF:
            pdf_data = generate_task_time_spent_pdf()

            result = Response(
                pdf_data,
                mimetype="application/pdf",
                headers={"Content-Disposition": "attachment;filename=task_report.pdf"}
            )

        if not result:
            abort(400, description="There was an error generating the report.")

        return result

