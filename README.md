# tasks-api-flask

## Table of Contents
- [Description](#description)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Testing and Documentation](#testing-and-documentation)

## Description

This is a simple API that allows you to create, read, update, and delete tasks. It is built using Flask and SQLAlchemy.

You can:
- Manage tasks and their status
- Test basic user logic
- Generate reports in JSON, Graph, and PDF formats for data analysis

## Prerequisites
- Python 3.x installed
- `pip` (Python package installer)

## Installation

1. Clone the repository
```bash
git clone git@github.com:Avepy/tasks-api-flask.git
```
2. Install the dependencies
```bash
pip install -r requirements.txt
```

3. Perform the database migrations
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

4. Run the application
```bash
python app.py
```

## Testing and Documentation
The API documentation can be easily accessed by accessing Swagger UI.
The link is printed out in the console when the application starts.