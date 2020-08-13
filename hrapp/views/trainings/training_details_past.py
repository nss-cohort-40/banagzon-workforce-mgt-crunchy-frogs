import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram, Employee
from ..connection import Connection

def get_training(training_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id training_id,
            t.title,
            t.description,
            t.start_date,
            t.end_date,
            t.capacity,
            et.id,
            et.employee_id,
            et.training_program_id,
            e.id,
            e.first_name,
            e.last_name
        FROM hrapp_trainingprogram t
        LEFT JOIN hrapp_employeetrainingprogram et ON et.training_program_id = t.id
        LEFT JOIN hrapp_employee e ON et.employee_id = e.id
        WHERE t.id = ?
        """, (training_id,))

        return db_cursor.fetchall()

@login_required
def training_details_past(request, training_id):
    if request.method == 'GET':
        training = get_training(training_id)
        template_name = 'trainings/detail_past.html'
        return render(request, template_name, {'training': training})
