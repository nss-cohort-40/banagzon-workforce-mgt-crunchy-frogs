from django.shortcuts import render, redirect, reverse
import sqlite3
from django.contrib.auth.decorators import login_required
from ..connection import Connection



def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.make,
            c.manufacturer,
            c.purchase_date,
            c.decommission_date,
            ec.computer_id,
            ec.employee_id,
            ec.assign_date,
            ec.unassign_date,
            e.id employees_id,
            e.first_name,
            e.last_name,
            e.department_id,
            d.id dept_id,
            d.dept_name
        FROM hrapp_computer c
        LEFT JOIN hrapp_employeecomputer ec on ec.computer_id = c.id
        LEFT JOIN hrapp_employee e on e.id = ec.employee_id
        LEFT JOIN hrapp_department d on d.id = e.department_id
        WHERE c.id = ?;
        """, (computer_id,))

        return db_cursor.fetchone()


@login_required
def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)
        template = 'computers/details.html'
        context = {
            'computer': computer,
        }

        return render(request, template, context)

    if request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                SELECT 
                    ec.id,
                    ec.computer_id
                from hrapp_employeecomputer ec
                where ec.computer_id = ?;
                """, (computer_id,))

                if len(db_cursor.fetchall()) == 0:
                    db_cursor.execute("""
                        DELETE FROM hrapp_computer
                        WHERE id = ?
                    """, (computer_id,))

            return redirect(reverse('hrapp:computer_list'))