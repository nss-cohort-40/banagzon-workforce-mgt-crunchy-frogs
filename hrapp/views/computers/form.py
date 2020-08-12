from django.shortcuts import render
import sqlite3
from ..connection import Connection


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.last_name,
            e.first_name,
            ec.id connection_id,
            ec.computer_id,
            ec.employee_id
        from hrapp_employee e
        left join hrapp_employeecomputer ec on ec.employee_id = e.id;
        """)

        return db_cursor.fetchall()


def computer_form(request):
    if request.method == 'GET':
        employees =  get_employees()
        template = "computers/form.html"
        context = {
            "employees": employees
        }

        return render(request, template, context)
