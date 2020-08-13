from django.shortcuts import render, redirect, reverse
import sqlite3
from ..connection import Connection


def get_programs(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.start_date,
            t.capacity,
            t.title,
            etp.id as etp_id,
            etp.employee_id,
            etp.training_program_id
        FROM hrapp_trainingprogram t
        left JOIN hrapp_employeetrainingprogram etp on etp.training_program_id = t.id
        WHERE t.start_date >= (select date('now'))
        """)
        dataset = db_cursor.fetchall()
        
        programs_employee_is_in = list()
        program_dict = dict()
        for row in dataset:
            if row["employee_id"] == employee_id:
                programs_employee_is_in.append(row["training_program_id"])
            if row["id"] not in program_dict:
                program_dict[row["id"]] = [row]
            else:
                program_dict[row["id"]].append(row)

        program_list = list()
        for program in program_dict:
            if len(program_dict[program]) < program_dict[program][0]["capacity"] and program not in programs_employee_is_in:
                program_list.append(program_dict[program][0])

        return program_list


def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name
        FROM hrapp_employee e
        WHERE e.id = ?;
        """, (employee_id,))
        return db_cursor.fetchone()

def assign_employee(request, employee_id):
    if request.method == 'GET':
        employee_training = {
            "employee": get_employee(employee_id),
            "training": get_programs(employee_id)
        }
        template = "employees/assign_program.html"
        context = {
            "employee_training": employee_training
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            if form_data["program_id"] != "":
                db_cursor.execute("""
                INSERT INTO hrapp_employeetrainingprogram (employee_id, training_program_id)
                VALUES(? , ?);
                """, (employee_id, form_data["program_id"]))

        return redirect(reverse('hrapp:employee_list'))
