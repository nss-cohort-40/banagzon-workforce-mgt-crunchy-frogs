<<<<<<< HEAD
INSERT INTO hrapp_trainingprogram(title, description, start_date, end_date, capacity)
VALUES("Demo Program", "This is a demo program for example purposes.", "2020-11-11", "2020-11-12", 50);

INSERT INTO hrapp_trainingprogram(title, description, start_date, end_date, capacity)
VALUES("Test Training", "Welcome to Test Training, where your mind will be pushed to its limit.", "2015-05-15", "2015-06-15", 15);
=======
INSERT INTO hrapp_employee(first_name, last_name, start_date, is_supervisor, department_id)
VALUES("Fel", "Mou", '12-12-2019', False, 2);


select
    e.id,
    e.first_name,
    e.last_name,
    e.start_date,
    e.is_supervisor
from hrapp_employee e;


INSERT INTO hrapp_department(dept_name, budget)
VALUEs("Construction", 2000000);



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


select
    d.id,
    d.dept_name,
    d.budget
from hrapp_department d;


INSERT INTO hrapp_computer (purchase_date, decomission_date, manufacturer, make)
VALUES("08/11/2020", "08/11/2024", "Dell", "Zephyr");


INSERT INTO hrapp_employeecomputer (computer_id, employee_id, assign_date, unassign_date)
VALUES(1, 1, "8/11/2020", "12/11/2020");


SELECT
    c.id,
    c.manufacturer,
    c.make,
    ec.id connection_id,
    ec.computer_id,
    ec.employee_id
from hrapp_computer c
left join hrapp_employeecomputer ec on ec.computer_id = c.id; 
>>>>>>> master
