from models.user import *
from sqlalchemy import Enum as SQLAlchemyEnum, func
from extensions import db
from enums.task_status import TaskStatus

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.OPEN, nullable=False)
    time_spent = db.Column(db.Float, default=0.0)
    date_started_at = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=func.now())
    date_modified = db.Column(db.DateTime, onupdate=func.now())
    date_deleted = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="tasks")

    def __init__(self, title, description, status=TaskStatus.OPEN):
        self.title = title
        self.description = description
        self.status = status

