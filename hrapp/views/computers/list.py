import sqlite3
from django.shortcuts import render, redirect, reverse
from ..connection import Connection
from hrapp.models import Computer
import datetime

def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT c.id,
            c.purchase_date,
            c.decommission_date,
            c.manufacturer,
            c.make
            from hrapp_computer c;
            """)

            computers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                computer = Computer()
                computer.id = row["id"]
                computer.purchase_date = row["purchase_date"]
                computer.decommission_date = row["decommission_date"]
                computer.manufacturer = row["manufacturer"]
                computer.make = row["make"]
                computers.append(computer)

        template = 'computers/list.html'
        context = {
            'computers': computers
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_computer (purchase_date, decommission_date, manufacturer, make)
            VALUES(?, ?, ?, ?);
            """, (form_data['purchase_date'], form_data['decommission_date'], form_data['manufacturer'], form_data['make']))

            if form_data["employee_id"] != "":
                db_cursor.execute("""
                SELECT
                    c.id,
                    c.make
                FROM hrapp_computer c
                ORDER BY c.id DESC;
                """)

                dataset = db_cursor.fetchall()

                db_cursor.execute("""
                INSERT INTO hrapp_employeecomputer (computer_id, employee_id, assign_date, unassign_date)
                VALUES(?, ?, ?, ?);
                """, (dataset[0][0], form_data["employee_id"], datetime.date.today(), datetime.date.today() + datetime.timedelta(days=90)))

        return redirect(reverse('hrapp:computer_list'))