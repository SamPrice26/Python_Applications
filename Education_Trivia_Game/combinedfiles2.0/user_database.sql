-- Creating the database for users in game (teachers, students, and parents)
CREATE DATABASE user_database;
USE user_database;

-- Adding teacher info table
CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,  
    subject VARCHAR(50) NOT NULL
);

-- Adding student info table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,  
    teacher_id INTEGER REFERENCES teachers(id)
);

-- Adding parent info table 
CREATE TABLE parents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,  
    student_id INTEGER REFERENCES students(id)
);

-- Inserting teacher info into table
INSERT INTO teachers (id, username, email, password, subject) VALUES 
(1, 'Miss. Grotke', 'historybuff68@thirdstreet.com', '$2b$12$7kgo1KoQnIyqBj4JP7JACuDBiiJ/gF3Mlix9p4WcmcvYdEbzBEOuK', 'History'),
(2, 'Miss. Finster', 'ihatekids@thirdstreet.com', '$2b$12$llQn/FIaPqVwUR/6mKyToeAgHxa2QuvaXHoSOJHJc4JpvwXH/LyBa', 'Physical Education'),
(3, 'Principal Prickly', 'pricklypear@thirdstreet.com', '$2b$12$FINEJAd/KGFEEOsY0y/8s..oHw6r9go472X8cjUFX9aiv7/Ak9qVu', 'Administration'),
(4, 'Mr. E', 'thescienceguy@thirdstreet.com', '$2b$12$k6D6kNamXVSp6zTqvkNGtuLQL/SjRdXmMMbSVgwWPN7gGpTgD.XAq', 'Science'),
(5, 'Mrs. Lemon', 'lovelylemon@thirdstreet.com', '$2b$12$HV2Y6NeC6QrKbmXMMiuZ..pV.l6bc5a.fuoQXUN5bW1lE55SAg//K', 'Maths'),
(6, 'Coach Kloogie', 'gosports@thirdstreet.com', '$2b$12$VA73c4TNBczJAS1iaTUQr.ahg.uLV4hDwolyFFX2SUQiFL66E0JCm', 'Sports'),
(7, 'Miss. Alordayne', 'whatisakilomenter@thirdstreet.com', '$2b$12$XSgHwOGyRmJPKtSDmtCYU.ejB67zUTT//M7Er.waZGTxb14RZiFE6', 'Geography'),
(8, 'Mr. Wordsworth', 'wordsworth@school.edu', '$2b$12$SzQw8n3CIFgeGzOXr7UB5uwLNwoYf5qvSao750Wri86nm7TafNeKq', 'English');

-- Inserting student info into table 
INSERT INTO students (id, username, email, password, teacher_id) VALUES 
(1, 'Theodor J. Detweiler', 'tj@thirdstreet.com', '$2b$12$C4X0vHD7H9OCwfewtJcHhuYIktxpsLdW0lsYHztqMNwjvdeh5NsN6', 1),
(2, 'Ashley Spinelli', 'notanotherashley@thirdstreet.com', '$2b$12$rYP0vPmadBL9Vfhq0IXkdeCCUA4Gb7MLrItdYNWEhqJ.kEJy/8oI.', 2),
(3, 'Gretchen Grundler', 'smartypants@thirdstreet.com', '$2b$12$ckP6lgDiBBsBtWgYdlsw1uAshvSeQMIlm6PwqONI6Uvf335/OLl2K', 1),
(4, 'Mikey Blumberg', 'mikey@thirdstreet.com', '$2b$12$gkd1zeT3M6HJ5clsz9gxK.77plTeF8igIkC9aJd0tHOv/aEz1A0KK', 1),
(5, 'Vince LaSalle', 'vince@thirdstreet.com', '$2b$12$rsLxnWGKfaMbvF7gbzfneO.6Ztuc4RgzItVW1zhMkO6XmPjunrUhC', 6),
(6, 'Gus Griswald', 'gus@thirdstreet.com', '$2b$12$OVa.EWDXtVVjKlh0gf0WSuGequZk0AQ66qNy91iEXjit4dlVnCqSa', 4),
(7, 'Robert King', 'kingbob@thirdstreet.com', '$2b$12$YlraBKgKsPL2YV.eXM20LeB.eqhpySQBX/W8oABqnWFAjw7lSYWVi', 3),
(8, 'TestStudent', 'teststudent@gmail.com', '68eaeeaef51a40035b5d3705c4e0ffd68036b6b821361765145f410b0f996e11', 5);

-- Inserting parent info into table 
INSERT INTO parents (id, username, email, password, student_id) VALUES 
(1, 'Mrs. Detweiler', 'mrdetweiler@thirdstreet.com', '$2b$12$DN/z6MSAck0YRNPjWLb8qORUjknmPIUciMseiUfPsLwdI.2SC6T5q', 1),
(2, 'Mrs. Spinelli', 'mrsspinelli@thirdstreet.com', '$2b$12$f8AP/dJqi3NvjOfFD54x0ekYbI2GkMqJp6XJz69C7BFqZyjH0OuhS', 2),
(3, 'Mrs. Grundler', 'mrgrundler@thirdstreet.com', '$2b$12$8t0tdQXxsM4w3leMinQoKOiFliM2aEdKcriVk1WdwLw679TGWgIsq', 3),
(4, 'Mrs. Blumberg', 'mrsblumberg@thirdstreet.com', '$2b$12$5mdnznORrKWWbBaiZv6Dtuhqv05YiKyFzSQ1e5v1ub1TUhNYJDiV6', 4),
(5, 'Mrs. Lasalle', 'mrlasalle@thirdstreet.com', '$2b$12$dbVdxZ4WPU07Cj47pRvyNeAhH56ijwpBX97ZfVKXbBVU2Ye7TU9Ri', 5),
(6, 'Mr. Griswald', 'mrsgriswald@thirdstreet.com', '$2b$12$v7vGRPWXs9gKI9.66dkCdOJ.IRmaVXzuI6Kl.KkLFSyyyrTkdtZvO', 6),
(7, 'Mrs. King', 'mrsking@thirdstreet.com', '$2b$12$f7LmQAJmcRWvIPlK6SrrTuHPZyYMznADAMBdhyuixiJKp/CdtSWAO', 7);

-- Creating a view so other members of the dev team can easily view info 
CREATE VIEW student_overview AS
SELECT 
    students.id AS student_id,
    students.username AS student_name,
    students.email AS student_email,
    teachers.username AS teacher_name,
    teachers.email AS teacher_email,
    teachers.subject AS teacher_subject,
    parents.username AS parent_name,
    parents.email AS parent_email
FROM 
    students
JOIN 
    teachers ON students.teacher_id = teachers.id
JOIN 
    parents ON students.id = parents.student_id;

-- Display the view
SELECT * FROM student_overview;
