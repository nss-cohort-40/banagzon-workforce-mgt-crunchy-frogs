import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department, Computer, EmployeeComputer, TrainingProgram, EmployeeTrainingProgram
from ..connection import Connection

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
    computer.make = _row["c_make"]

    training_program = TrainingProgram()
    training_program.id = _row["tp_id"]
    training_program.title = _row["tp_title"]

    employee.department = department
    employee.training_program = training_program

    return employee

@login_required
def get_employee(employee_id):
    if request.method == 'GET':
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
                c.id,
                c.make,
                etp.id,
                etp.employee_id,
                etp.training_program_id,
            from hrapp_employee e
            left join hrapp_department d on d.id = e.department_id
            left join hrapp_employeecomputer ec on ec.employee_id = e.id
            left join hrapp_computer c on ec.computer_id = c.id;
            left join hrapp_employeetrainingprogram etp on etp.employee_id = e.id
            left join hrapp_trainingprogram tp on etp.training_program_id = tp.id
            """)
            # TODO: Check the training_program_id

            return db_cursor.fetchone()
