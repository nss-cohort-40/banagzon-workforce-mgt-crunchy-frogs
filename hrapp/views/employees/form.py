from django.shortcuts import render
import sqlite3
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


def employee_edit_form(request, employee_id):

    if request.method == 'GET':
        employee = Employee.objects.filter(id=employee_id)
        departments = Department.objects.all()
        department = Department.objects.filter(id=employee[0].department_id)
        computer = len(EmployeeComputer.objects.filter(
            employee_id=employee[0].id))
        template = 'employees/form.html'
        if computer > 0:
            EmployeeComputer.objects.filter(employee_id=employee[0].id)
            computer = EmployeeComputer.objects.filter(
                employee_id=employee[0].id)
            # computer = Computer.objects.filter(id=computer[0].computer_id)
            computer = EmployeeComputer.objects.filter(employee_id=employee_id)
            context = {
                'employee': employee[0],
                'department': department[0],
                'departments': departments,
                'computers': get_computers(),
                'start_date': str(employee[0].start_date),
                'computer': computer[0]
            }
        else:
            context = {
                'employee': employee[0],
                'department': department[0],
                'departments': departments,
                'computers': get_computers(),
                'start_date': str(employee[0].start_date),
                'computer': ""
            }
        return render(request, template, context)
