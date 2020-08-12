import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from ..connection import Connection

def trainings_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                t.id,
                t.title,
                t.description,
                t.start_date,
                t.end_date,
                t.capacity
            from hrapp_trainingProgram t
            where t.start_date >= (select date('now'))
            """)

            trainings = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                training = TrainingProgram()
                training.id = row['id']
                training.title = row['title']
                training.description = row['description']
                training.start_date = row['start_date']
                training.end_date = row['end_date']
                training.capacity = row['capacity']

                trainings.append(training)

            template = 'trainings/trainings_list.html'
            context = {
                'all_trainings': trainings
            }

            return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingProgram
            (
                title, description, start_date,
                end_date, capacity
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['description'],
                form_data['start_date'], form_data['end_date'],
                form_data["capacity"]))

        return redirect(reverse('hrapp:trainings_list'))