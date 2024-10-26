from matplotlib import pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timezone
from sqlalchemy import func, desc, asc
from sqlalchemy.exc import IntegrityError

from controllers.user_controller import get_user_by_id
from enums.task_status import TaskStatus
from enums.order_type import OrderType


from models.task import Task, db


def get_all_tasks(status=None, sort_by=None, order=OrderType.ASC):
    """Get all tasks that are not soft-deleted, with optional filtering and sorting."""
    query = Task.query.filter_by(date_deleted=None)

    if status:
        query = query.filter(Task.status == status)

    if sort_by:
        if order == OrderType.DESC:
            query = query.order_by(desc(getattr(Task, sort_by, 'id')))
        else:
            query = query.order_by(asc(getattr(Task, sort_by, 'id')))

    print(f"query: {query}")

    return query.all()



def get_task_by_id(task_id):
    """Get a task by its ID if not soft-deleted."""
    return Task.query.filter_by(id=task_id, date_deleted=None).first()


def create_task(title, description=""):
    """Create a new task."""
    try:
        new_task = Task(title=title, description=description)

        db.session.add(new_task)
        db.session.commit()

        return new_task
    except IntegrityError:
        db.session.rollback()
        return None


def delete_task(task_id):
    """Soft delete a task by setting its date_deleted."""
    task = get_task_by_id(task_id)

    if task:
        task.date_deleted = func.now()
        db.session.commit()
        return task

    return None


def update_task_status(task_id, new_status_value):
    """Update a task's status and related fields."""
    task = get_task_by_id(task_id)
    if not task:
        return None, 404

    try:
        new_status = TaskStatus(new_status_value)
    except ValueError:
        return None, 400

    if new_status == task.status:
        return None, 400

    now = datetime.now(timezone.utc)

    if new_status == TaskStatus.PENDING:
        task.status = TaskStatus.PENDING
        task.date_started_at = now
    elif new_status == TaskStatus.COMPLETED:
        task.status = TaskStatus.COMPLETED

        if task.date_started_at:
            if task.date_started_at.tzinfo is None:
                task.date_started_at = task.date_started_at.replace(tzinfo=timezone.utc)
            task.time_spent = (now - task.date_started_at).total_seconds()
        else:
            task.time_spent = 0

    elif new_status == TaskStatus.OPEN:
        task.status = TaskStatus.OPEN
        task.time_spent = 0

    db.session.commit()

    return task, 200


def assign_task_to_user(task_id, user_id):
    """Assign a task to a user."""
    task = get_task_by_id(task_id)
    if not task:
        return None, 404

    user = get_user_by_id(user_id)
    if not user:
        return None, 404

    try:
        task.user_id = user_id
        db.session.commit()

        return task, 200
    except IntegrityError:
        db.session.rollback()
        return None, 400


def format_time_spent(total_seconds):
    """Convert time in seconds to 'D H:M:SS' format."""
    total_seconds = int(total_seconds)

    days = total_seconds // (24 * 3600)
    total_seconds %= (24 * 3600)

    hours = total_seconds // 3600
    total_seconds %= 3600

    mins = total_seconds // 60
    secs = total_seconds % 60

    if days > 0:
        return f"{days}d {hours}h {mins:02d}m {secs:02d}s"
    elif hours > 0:
        return f"{hours}h {mins:02d}m {secs:02d}s"
    else:
        return f"{mins}m {secs:02d}s"


def get_task_time_spent_report():
    """Get a report of time spent on every task."""
    tasks = Task.query.filter(
        Task.date_deleted.is_(None),
        Task.time_spent > 0
    ).all()

    report_data = [
        {
            'task_id': task.id,
            'title': task.title,
            'time_spent': format_time_spent(task.time_spent),
            'user_id': task.user_id,
            'username': task.user.username if task.user else None,
            'status': task.status.value,
        }
        for task in tasks
    ]

    return report_data


def generate_task_time_spent_graph():
    """Generate a graph of time spent on every task with adaptive time units."""
    tasks = Task.query.filter(
        Task.date_deleted.is_(None),
        Task.time_spent > 0
    ).all()

    if not tasks:
        return None

    task_titles = []
    time_spent_seconds = []

    for task in tasks:
        task_titles.append(task.title)
        time_spent_seconds.append(task.time_spent)

    max_time_spent = max(time_spent_seconds)

    if max_time_spent >= 86400:  # 1 day
        time_unit = 'days'
        time_spent = [t / 86400 for t in time_spent_seconds]
        ylabel = "Time Spent (days)"
    elif max_time_spent >= 3600:  # 1 hour
        time_unit = 'hours'
        time_spent = [t / 3600 for t in time_spent_seconds]
        ylabel = "Time Spent (hours)"
    else:
        time_unit = 'minutes'
        time_spent = [t / 60 for t in time_spent_seconds]  # 1 minute
        ylabel = "Time Spent (minutes)"

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.bar(task_titles, time_spent, color="skyblue")
    plt.xlabel("Task")
    plt.ylabel(ylabel)
    plt.title(f"Time Spent on Tasks ({time_unit.capitalize()})")
    plt.xticks(rotation=45, ha="right")

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return buf.getvalue()


def generate_task_time_spent_pdf():
    """Generate a PDF report of time spent on every task."""
    tasks = Task.query.filter(
        Task.date_deleted.is_(None),
        Task.time_spent > 0
    ).all()

    buffer = BytesIO()
    ctx = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    y = height - 50

    ctx.setFont("Helvetica-Bold", 14)
    ctx.drawString(50, y, "Task Time Spent Report")
    y -= 30

    ctx.setFont("Helvetica", 12)
    for task in tasks:
        ctx.drawString(50, y, f"Task ID: {task.id}")
        y -= 15
        ctx.drawString(50, y, f"Title: {task.title}")
        y -= 15
        ctx.drawString(50, y, f"Time Spent: {format_time_spent(task.time_spent)}")
        y -= 15
        ctx.drawString(50, y , f"User ID: {task.user_id}")
        y -= 30

        if y < 50:
            ctx.showPage()
            y = height - 50

    ctx.save()
    buffer.seek(0)

    return buffer.getvalue()

