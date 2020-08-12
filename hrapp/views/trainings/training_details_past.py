import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram
from ..connection import Connection


def create_training(cursor, row):
    _row = sqlite3.Row(cursor, row)

    training = TrainingProgram()
    training.id = _row["training_id"]
    training.title = _row["title"]
    training.description = _row["description"]
    training.start_date = _row["start_date"]
    training.end_date = _row["end_date"]
    training.capacity = _row["capacity"]

    return training


def get_training(training_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_training
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id training_id,
            t.title,
            t.description,
            t.start_date,
            t.end_date,
            t.capacity
        FROM hrapp_trainingprogram t
        WHERE t.id = ?
        """, (training_id,))

        return db_cursor.fetchone()

@login_required
def training_details_past(request, training_id):
    if request.method == 'GET':
        training = get_training(training_id)
        template_name = 'trainings/detail.html'
        return render(request, template_name, {'training': training})
