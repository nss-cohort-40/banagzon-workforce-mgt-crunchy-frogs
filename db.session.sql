

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
    (null, 'Kirk', 'Suddath', '2020-05-02', FALSE, 10);

select
    d.id,
    d.dept_name,
    d.budget
from hrapp_department d;


DELETE FROM hrapp_department
where id = 9;

SELECT
    d.id,
    d.dept_name,
    d.budget,
    e.first,
    e.last,
    e.department_id
FROM hrapp_department d
    join hrapp_employee e on d.id = e.department_id;
        

