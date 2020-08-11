import sqlite3
import datetime
from django.shortcuts import render, redirect, reverse
from hrapp.models import Employee
from ..Connection import Connection

def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # TODO: Add to query: e.department,
            db_cursor.execute("""
            select
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                e.department_id,
                ec.id,
                ec.computer_id,
                ec.employee_id,
                d.id as dept_id,
                d.dept_name,
                d.budget,
                c.id,
                c.manufacturer,
                c.make
            from hrapp_employee e
            left join hrapp_department d on d.id = e.department_id
            left join hrapp_employeecomputer ec on ec.employee_id = e.id
            left join hrapp_computer c on ec.computer_id = c.id;
            """)

            all_employees = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                employee = Employee()
                employee.id = row['id']
                employee.first_name = row['first_name']
                employee.last_name = row['last_name']
                employee.start_date = row['start_date']
                employee.is_supervisor = row['is_supervisor']
                employee.dept_name = row['dept_name']
                employee.computer = row['make']

                all_employees.append(employee)

        template = 'employees/employees_list.html'
        context = {
            'employees': all_employees
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_employee(first_name, last_name, start_date, is_supervisor, department_id)
            VALUES(?, ?, ?, ?, ?);
            """, (form_data['first_name'], form_data['last_name'], form_data['start_date'], bool(int(form_data['is_supervisor'])), form_data['department_id']))

            db_cursor.execute("""
            SELECT
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor
            FROM hrapp_employee e
            ORDER BY e.id DESC;
            """)

            dataset = db_cursor.fetchall()

            db_cursor.execute("""
            INSERT INTO hrapp_employeecomputer (computer_id, employee_id, assign_date, unassign_date)
            VALUES(?, ?, ?, ?);
            """, (form_data['computer_id'], dataset[0][0], datetime.date.today(), datetime.date.today() + datetime.timedelta(days=90)))

            

        return redirect(reverse('hrapp:employee_list'))