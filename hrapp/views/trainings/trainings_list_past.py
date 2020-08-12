import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from ..connection import Connection

def trainings_list_past(request):
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
            where t.start_date < (select date('now'))
            """)

            past_trainings = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                training = TrainingProgram()
                training.id = row['id']
                training.title = row['title']
                training.description = row['description']
                training.start_date = row['start_date']
                training.end_date = row['end_date']
                training.capacity = row['capacity']

                past_trainings.append(training)

            template = 'trainings/trainings_list_past.html'
            context = {
                'past_trainings': past_trainings
            }

            return render(request, template, context)