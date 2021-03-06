from django.shortcuts import render
import sqlite3
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Employee, Department, Computer, EmployeeComputer


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

@login_required
def employee_form(request):
    if request.method == 'GET':
        departments_computers = {
            "departments": get_departments(),
            "computers": get_computers()
        }
        template = "employees/form.html"
        context = {
            "departments_computers": departments_computers
        }

        return render(request, template, context)


def get_employee_computer(employee_idd):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select ec.id, ec.employee_id, c.make
        from hrapp_employeecomputer ec
            join hrapp_computer c on c.id = ec.computer_id
        where employee_id = ?
                """, (employee_idd,))

        return db_cursor.fetchone()


def employee_edit_form(request, employee_idd):
    print('computer1')
    if request.method == 'GET':
        employee = Employee.objects.filter(id=employee_idd)
        departments = Department.objects.all()
        department = Department.objects.filter(id=employee[0].department_id)
        computer = get_employee_computer(employee_idd)

        template = 'employees/form.html'

        context = {
            'employee': employee[0],
            'department': department[0],
            'departments': departments,
            'computers': get_computers(),
            'start_date': str(employee[0].start_date),
            'computer': computer
        }
        return render(request, template, context)
