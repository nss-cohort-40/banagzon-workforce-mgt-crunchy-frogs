from django.shortcuts import render
import sqlite3
from ..Connection import Connection


def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.dept_name,
            d.budget
        from hrapp_department d
        """)

        return db_cursor.fetchall()


def employee_form(request):
    if request.method == 'GET':
        departments_computers = {
            "departments" : get_departments(),
            "computers" : 
        }
        template = "employees/form.html"
        context = {
            "departments_computers": departments
        }

        return render(request, template, context)
