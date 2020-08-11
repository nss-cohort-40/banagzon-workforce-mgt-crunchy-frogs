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


def get_computers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.manufacturer,
            c.make,
            ec.id connection_id,
            ec.computer_id,
            ec.employee_id
        from hrapp_computer c
        left join hrapp_employeecomputer ec on ec.computer_id = c.id;
        """)

        return db_cursor.fetchall()

def employee_form(request):
    if request.method == 'GET':
        departments_computers = {
            "departments" : get_departments(),
            "computers" : get_computers()
        }
        template = "employees/form.html"
        context = {
            "departments_computers": departments_computers
        }

        return render(request, template, context)
