INSERT INTO hrapp_employee(first_name, last_name, start_date, is_supervisor)
VALUES("Zach", "Attack", '12-12-2019', False);


select
    e.id,
    e.first_name,
    e.last_name,
    e.start_date,
    e.is_supervisor
from hrapp_employee e