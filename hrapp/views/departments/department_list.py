import sqlite3
from django.shortcuts import render
from hrapp.models import Department, Employee
from ..connection import Connection


def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select distinct
                d.id,
                d.dept_name,
                d.budget,
                e.department_id
            from hrapp_department d
                join hrapp_employee e on d.id = e.department_id;
            """)

            all_departments = []
            dataset = db_cursor.fetchall()
            count = {}

            for row in dataset:
                department = Department()
                employee = Employee()
                department.id = row['id']
                department.dept_name = row['dept_name']
                department.budget = row['budget']
                employee.department_id = row['department_id']
                department.count = len(
                    Employee.objects.filter(department_id=department.id))
                all_departments.append(department)

    template = 'departments/department_list.html'
    context = {
        'all_departments': all_departments
    }

    return render(request, template, context)
