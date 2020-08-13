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

def training_details(request, training_id):
    if request.method == 'GET':
        training = get_training(training_id)
        template_name = 'trainings/detail.html'
        return render(request, template_name, {'training': training})

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_trainingprogram
                SET title = ?,
                    description = ?,
                    start_date = ?,
                    end_date = ?,
                    capacity = ?
                WHERE id = ?
                """,
                (
                    form_data['title'], form_data['description'],
                    form_data['start_date'], form_data['end_date'],
                    form_data['capacity'], training_id,
                ))

            return redirect(reverse('hrapp:trainings_list'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM hrapp_trainingprogram
                    WHERE id = ?
                """, (training_id,))

            return redirect(reverse('hrapp:trainings_list'))