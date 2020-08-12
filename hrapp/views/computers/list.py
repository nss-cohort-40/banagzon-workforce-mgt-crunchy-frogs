import sqlite3
from django.shortcuts import render, redirect, reverse
from ..Connection import Connection
from hrapp.models import Computer

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