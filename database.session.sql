INSERT INTO hrapp_trainingprogram(title, description, start_date, end_date, capacity)
VALUES("Demo Program", "This is a demo program for example purposes.", "2020-11-11", "2020-11-12", 50);

INSERT INTO hrapp_trainingprogram(title, description, start_date, end_date, capacity)
VALUES("Test Training", "Welcome to Test Training, where your mind will be pushed to its limit.", "2015-05-15", "2015-06-15", 15);

INSERT INTO hrapp_employeetrainingprogram(employee_id, training_program_id)
VALUES(1, 3);
INSERT INTO hrapp_employeetrainingprogram(employee_id, training_program_id)
VALUES(2, 3);

SELECT
    t.id training_id,
    t.title,
    t.description,
    t.start_date,
    t.end_date,
    t.capacity,
    et.id,
    et.employee_id,
    et.training_program_id,
    e.id,
    e.first_name,
    e.last_name
FROM hrapp_trainingprogram t
LEFT JOIN hrapp_employeetrainingprogram et ON et.training_program_id = t.id
LEFT JOIN hrapp_employee e ON et.employee_id = e.id