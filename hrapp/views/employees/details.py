import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department, Computer, EmployeeComputer, TrainingProgram, EmployeeTrainingProgram
from ..connection import Connection
import datetime


def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    employee = Employee()
    employee.id = _row["e_id"]
    employee.first_name = _row["e_first_name"]
    employee.last_name = _row["e_last_name"]

    department = Department()
    department.id = _row["d_id"]
    department.name = _row["d_name"]

    computer = Computer()
    computer.id = _row["c_id"]
    computer.make = _row["make"]

    # employee.training_programs = []
    employee.department = department
    employee.computer = computer

    return employee


def get_training_programs(employee_id):
    training_programs_ids = []
    training_programs_ids = EmployeeTrainingProgram.objects.filter(
        employee_id=employee_id)
    training_programs = []
    for e in training_programs_ids:
        training_program = TrainingProgram.objects.filter(
            id=e.training_program_id).values()
        for i in training_program:
            training_programs.append(i["title"])

    return training_programs


def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_employee
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select
                e.id as e_id,
                e.first_name as e_first_name,
                e.last_name as e_last_name,
                e.department_id,
                ec.id,
                ec.computer_id,
                ec.employee_id,
                d.id as d_id,
                d.dept_name as d_name,
                c.id as c_id,
                c.make
            from hrapp_employee e
            left join hrapp_department d on d.id = e.department_id
            left join hrapp_employeecomputer ec on ec.employee_id = e.id
            left join hrapp_computer c on ec.computer_id = c_id
            left join hrapp_employeetrainingprogram etp on etp.employee_id = e.id
            left join hrapp_trainingprogram tp on etp.training_program_id = tp.id
            where e.id = ?
            """, (employee_id,))

        return db_cursor.fetchone()


@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        training_programs = get_training_programs(employee_id)
        template = 'employees/details.html'
        context = {
            'employee': employee,
            'training_programs': training_programs
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing an employee
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_employee
                SET first_name = ?,
                    last_name = ?,
                    start_date = ?,
                    is_supervisor = ?,
                    department_id = ?
                WHERE id = ?
                """,
                                  (
                                      form_data['first_name'], form_data['last_name'],
                                      form_data['start_date'], form_data['is_supervisor'],
                                      form_data["department_id"], employee_id,
                                  ))

                db_cursor.execute("""
                UPDATE hrapp_employeecomputer
                SET computer_id = ?
                WHERE employee_id = ?
                """,
                                  (
                                      form_data['computer_id'], employee_id,
                                  ))
        elif (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT and POST"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_employee
                SET first_name = ?,
                    last_name = ?,
                    start_date = ?,
                    is_supervisor = ?,
                    department_id = ?
                WHERE id = ?
                """,
                                  (
                                      form_data['first_name'], form_data['last_name'],
                                      form_data['start_date'], form_data['is_supervisor'],
                                      form_data["department_id"], employee_id,
                                  ))

                db_cursor.execute("""
                insert into hrapp_employeecomputer
                values (?,?,?,?,?)
                
                """,
                                  (
                                      None, datetime.datetime.now(), datetime.datetime.now() +
                                      datetime.timedelta(days=90),
                                      form_data['computer_id'], employee_id,
                                  ))

            return redirect(reverse('hrapp:employee_list'))
