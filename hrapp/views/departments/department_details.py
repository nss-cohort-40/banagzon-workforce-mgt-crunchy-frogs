import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Employee


def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.dept_name,
            d.budget
        FROM hrapp_department d
        WHERE d.id = ?
        """, (department_id,))

        return db_cursor.fetchone()


def department_details(request, department_id):
    if request.method == 'GET':
        department = get_department(department_id)
        employees = []
        employees = Employee.objects.filter(department_id=department_id)
        template = 'departments/department_details.html'
        context = {
            'department': department,
            'employees': employees
        }

        return render(request, template, context)
