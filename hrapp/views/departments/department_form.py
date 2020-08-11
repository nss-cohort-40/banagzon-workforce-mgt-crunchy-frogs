import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Department
from ..connection import Connection


def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.dept_name
        from hrapp_department d
        """)

        return db_cursor.fetchall()


@login_required
def department_form(request):
    if request.method == 'GET':
        all_departments = get_departments()
        template = 'departments/department_form.html'
        context = {
            'all_departments': all_departments
        }

        return render(request, template, context)
