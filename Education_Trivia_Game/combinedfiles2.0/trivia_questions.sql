-- Create the game questions database
CREATE DATABASE trivia_questions;
USE trivia_questions;

-- Subjects Table
CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) UNIQUE NOT NULL
);

-- Questions Table
CREATE TABLE questions (
    question_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    difficulty_level ENUM('easy', 'medium', 'hard') NOT NULL,
    question_text VARCHAR(255) NOT NULL,
    option_a VARCHAR(100) NOT NULL,
    option_b VARCHAR(100) NOT NULL,
    option_c VARCHAR(100) NOT NULL,
    option_d VARCHAR(100) NOT NULL,
    correct_option CHAR(1) NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

-- Custom Questions Table
CREATE TABLE custom_questions (
    question_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,  -- No foreign key constraint to user_database
    question_text VARCHAR(255) NOT NULL,
    option_a VARCHAR(100) NOT NULL,
    option_b VARCHAR(100) NOT NULL,
    option_c VARCHAR(100) NOT NULL,
    option_d VARCHAR(100) NOT NULL,
    correct_option CHAR(1) NOT NULL,
    difficulty_level ENUM('easy', 'medium', 'hard') NOT NULL
);

-- Quizzes Table
CREATE TABLE quizzes (
    quiz_id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,  -- No foreign key constraint to user_database
    quiz_name VARCHAR(100) NOT NULL,
    subject_id INT NOT NULL,
    difficulty_level ENUM('easy', 'medium', 'hard') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

-- Quiz-Questions Mapping Table
CREATE TABLE quiz_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    question_id INT NOT NULL,
    question_source ENUM('custom', 'standard') NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

-- Scores Table
CREATE TABLE scores (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,  -- No foreign key constraint to user_database
    quiz_id INT NOT NULL,
    score INT NOT NULL,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
);

-- Quiz Results Table
CREATE TABLE quiz_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,  
    quiz_id INT NOT NULL,
    answers TEXT,
    score INT NOT NULL,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
);

-- Insert Subjects
INSERT INTO subjects (subject_name) VALUES ('Maths'), ('English');

-- Insert Sample Data into Questions Table
INSERT INTO questions (subject_id, difficulty_level, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
-- Maths Easy Questions
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'What is 2 + 3?', '4', '5', '6', '7', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'What is 10 - 4?', '5', '6', '7', '8', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'What shape has 3 sides?', 'Square', 'Triangle', 'Rectangle', 'Circle', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'What is 2 x 3?', '5', '6', '7', '8', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'What is half of 8?', '3', '4', '5', '6', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'If you have 3 apples and eat 1, how many apples are left?', '1', '2', '3', '4', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'Which number is even?', '3', '5', '6', '7', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'What is 10 divided by 2?', '3', '4', '5', '6', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'What is the next number after 6?', '5', '6', '7', '8', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'easy', 'How many sides does a square have?', '3', '4', '5', '6', 'B'),

-- Maths Medium Questions
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'What is 5 x 4?', '20', '25', '30', '35', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'If you have 15 candies and give away 7, how many do you have left?', '6', '7', '8', '9', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'Which fraction is equivalent to 1/2?', '2/4', '3/5', '4/6', '1/3', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'What is the perimeter of a square with each side 4 cm?', '8 cm', '12 cm', '16 cm', '20 cm', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'What is 9 x 6?', '48', '54', '56', '60', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'If a pizza is cut into 8 slices and you eat 3, what fraction of the pizza is left?', '3/8', '4/8', '5/8', '6/8', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'Which of these numbers is a multiple of 7?', '21', '24', '25', '28', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'What is 100 - 37?', '53', '63', '73', '83', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'What is the value of the digit 5 in the number 350?', '5', '50', '500', '5,000', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'medium', 'How many faces does a cube have?', '4', '5', '6', '8', 'C'),

-- Maths Hard Questions
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'What is 45 ÷ 5?', '7', '8', '9', '10', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'If a rectangle has a length of 8 cm and a width of 3 cm, what is its area?', '11 cm²', '22 cm²', '24 cm²', '28 cm²', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'What is the value of 3³?', '6', '9', '27', '81', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'How many degrees are in a right angle?', '45°', '60°', '90°', '120°', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'What is the next prime number after 7?', '8', '9', '10', '11', 'D'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'What is the least common multiple of 3 and 4?', '6', '8', '10', '12', 'D'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'If a triangle has sides of 3 cm, 4 cm, and 5 cm, what type of triangle is it?', 'Equilateral', 'Isosceles', 'Scalene', 'Right-angled', 'D'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'What is 18% of 200?', '18', '36', '54', '72', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'How many edges does a cube have?', '6', '8', '12', '16', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'Maths'), 'hard', 'What is the square root of 64?', '6', '7', '8', '9', 'C'),

-- English Easy Questions
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'What is the opposite of "cold"?', 'Warm', 'Hot', 'Cool', 'Freezing', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'What is the plural of "dog"?', 'Doges', 'Dogs', 'Doggies', 'Dogz', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'Which word is a verb?', 'Swim', 'Quick', 'Funny', 'Tall', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'What is the first letter in the word "elephant"?', 'E', 'L', 'P', 'T', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'Which word is an adjective?', 'Run', 'Quick', 'Ball', 'Laugh', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'What is the opposite of "happy"?', 'Sad', 'Excited', 'Joyful', 'Elated', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'Which word is a pronoun?', 'I', 'Apple', 'Tree', 'School', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'What is a synonym for "small"?', 'Tiny', 'Huge', 'Tall', 'Short', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'What is the opposite of "up"?', 'Left', 'Right', 'Down', 'Sideways', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'easy', 'Which of these is a sentence?', 'Blue sky.', 'Dog barks.', 'Apple red.', 'Tree tall.', 'B'),

-- English Medium Questions
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'What is the past tense of "go"?', 'Goed', 'Went', 'Gone', 'Goes', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'Which word is an adjective?', 'Sleep', 'Happy', 'Quickly', 'Run', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'What is the synonym of "angry"?', 'Mad', 'Sad', 'Joyful', 'Peaceful', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'Which word is a verb?', 'Sing', 'High', 'Bright', 'Apple', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'What is the plural of "mouse"?', 'Mouses', 'Mice', 'Mouses', 'Mice', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'What is the opposite of "tall"?', 'Short', 'Slim', 'Thin', 'Small', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'Which word is a noun?', 'Joy', 'Run', 'Fast', 'High', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'What is the antonym of "dark"?', 'Bright', 'Tall', 'Short', 'Heavy', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'What is a pronoun?', 'Fast', 'He', 'Bright', 'Tree', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'medium', 'What is a synonym for "brave"?', 'Cowardly', 'Bold', 'Quiet', 'Nervous', 'B'),

-- English Hard Questions
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'What is the antonym of "courageous"?', 'Bold', 'Timid', 'Fearless', 'Brave', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'What is the plural of "tooth"?', 'Tooths', 'Teeth', 'Toothes', 'Teet', 'B'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'Which word is a conjunction?', 'And', 'Happy', 'Fast', 'Tall', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'Which word is an antonym of "weak"?', 'Strong', 'Tough', 'Soft', 'Sturdy', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'What is a synonym for "chatty"?', 'Silent', 'Reserved', 'Talkative', 'Shy', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'Which word is a preposition?', 'Over', 'Bright', 'Quickly', 'Slowly', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'What is the antonym of "bright"?', 'Dim', 'Light', 'Dark', 'Heavy', 'C'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'Which word is an adjective?', 'Quick', 'Run', 'Walk', 'Sing', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'What is the antonym of "kind"?', 'Cruel', 'Gentle', 'Soft', 'Warm', 'A'),
((SELECT subject_id FROM subjects WHERE subject_name = 'English'), 'hard', 'Which word is a synonym for "intelligent"?', 'Dull', 'Bright', 'Ignorant', 'Lazy', 'B');
