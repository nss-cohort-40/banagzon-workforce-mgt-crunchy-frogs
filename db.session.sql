

INSERT INTO hrapp_department
VALUES
    (null, 'Coca Cola', 2000000000);
INSERT INTO hrapp_department
VALUES
    (null, 'Sunkist', 100000000);
INSERT INTO hrapp_department
VALUES
    (null, 'Sprite', 500000000);

INSERT INTO hrapp_employee
VALUES
    (null, 'Felipe', 'Moura', '2020-02-05', FALSE, 1);

INSERT INTO hrapp_employee
VALUES
    (null, 'Jesus', 'Vazquez', '2019-07-02', FALSE, 1);

INSERT INTO hrapp_employee
VALUES
    (null, 'John', 'Bain', '2020-02-14', FALSE, 2);

INSERT INTO hrapp_employee
VALUES
    (null, 'Zach', 'Nicholson', '2020-05-02', FALSE, 3);

INSERT INTO hrapp_employee
VALUES
    (null, 'Tanner', 'Brainard', '2020-05-02', FALSE, 4);

select
    d.id,
    d.dept_name,
    d.budget,
    e.department_id,
    e.first_name,
    e.last_name
from hrapp_department d
    join hrapp_employee e on d.id = e.department_id;

update hrapp_computer
set manufacturer = 'Apple'
where id = 3;

delete from hrapp_employeecomputer
where id = 19;


select ec.id, ec.employee_id, c.make
from hrapp_employeecomputer ec
    join hrapp_computer c on c.id = ec.computer_id
where employee_id = 2;

