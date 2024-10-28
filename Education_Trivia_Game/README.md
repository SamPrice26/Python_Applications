# Engineering-4 Group-4 Project
## Educational Trivia Game

<img src="https://logopond.com/logos/7cbefd1c803c7e9515ea4be59233da29.png" width="150">

This project is about creating a fun and interactive learning game for students who may not be able to attend class due to mental health constraints. It takes the form of a multiple-choice trivia game that covers various curriculum topics for primary school children. It incorporates the use of media to create variation, a sense of enjoyment and achievement through promoting positive engagement to boost the well-being of young people.

### Prerequisites
You will need to have PyCharm Community Edition and MySQL installed on your personal laptop 💻 or desktop 🖥️.

For more information about downloading and setting up PyCharm Community Edition, please see [PyCharm Downloads](https://www.jetbrains.com/pycharm/download/).

For more information about downloading and setting up MySQL, please see [MySQL Downloads](https://dev.mysql.com/downloads/mysql/).

### Instruction for Use
The list of package requirements can be found in the `requirements.txt` file, and to install it on your system you can follow the instructions below:

- Initialise a local git reposistory on your system then clone the remote GitHub repository to your local repository
```
git remote add origin git@github.com:MegThw/Engineering-4-Group-4-Project-Educational-Trivia-Game.git
```
- Install the dependencies directly from your Python console
```
import pip
pip.main(['install', '-r', 'requirements.txt'])
```
The directory structure is as follows:
```
-combinedfiles2.0
    -app.py
    -config.py
    -game.py
    -main.py
    -questions.py
    -requirements.txt
    -trivia_questions.sql
    -user.py
    -user_database.sql
    -utils.py
-unit test files
    -test_app.py
    -test_game.py
    -test_main.py
    -test_questions.py
    -test_user.py
-.gitignore
-Engineering4-Group 4 Activity log.xlsx
-Final Project Document.pdf
-README.md
```
- In your PyCharm, open the `combinedfiles2.0` folder and enter your *user* (if not the defualt 'root') and *password* information in the `config.py` file
```
DATABASE_CONFIG = {
    'user_db': {
        'host': 'localhost',
        'user': 'root',  # Replace with your MySQL username
        'password': '',  # Replace with your MySQL password
        'database': 'user_database'
    },
   'trivia_db': {
        'host': 'localhost',
        'user': 'root',  # Replace with your MySQL username
        'password': '',  # Replace with your MySQL password
        'database':  'trivia_questions'
    }
}
```

- Next, in the `combinedfiles2` folder, run the app.py file, then run the main.py file to get started

### Game Rules 📲🎮
The console app retrieves data about different educational trivia questions, including their subject name and id, difficulty level and an array of the correct and incorrect answer choices. 

Students will be able to select their subject choice from the current subjects provided: *English* and *Math*, and then select their difficulty level from the options 'easy', 'medium', 'hard' or 'any'. A set of 10 questions for their selected choice of subject and difficulty level will then be generated, and each question has a 30 second timer within which the student will need to provide an answer *A, B, C* or *D*.

<img src="https://a0.anyrgb.com/pngimg/972/1432/quiz-up-pics-quiz-guess-the-words-quiz-guess-word-trivia-history-quiz-trivia-games-quiz-game-100-pics-quiz-guess-the-trivia-games-current-affairs-online-quiz-trivia.png" width="150">

Student answers are recorded in a file for the student to be able to track their progress in the app at the end of each question set for further review. At the end of the game, students can see their total score in the console. Points are awarded for correct answers based on the difficulty level and the time taken to answer, whilst incorrect answers gain no points and instead feedback is given on the correct answer. Below is a demonstration of the score key:
```
Easy: 1-5 points
Medium: 3-7 points
Hard: 5-10 points
```
Students can earn achievements for completing subjects, reaching score milestones or for their answering streaks.
### User Features 🧑‍💻🤓📖
The Educational Trivia Game app is designed for use from students, teachers, parents and administration. The user functions provided for each type of user are outlined below:
#### Students 

- Starting a new quiz
- Tracking scores

#### Teachers 
- Creating new custom quizzes
- Updating existing quiz questions
- Tracking student scores

#### Parents
- Tracking child's scores

### Instructions for Creating User Account 🤖🖥️
The user is prompted for their user type (student, parent or teacher), after which they are prompted for a username, email address and a password. The user is then presented a menu based on their user type.

### Instructions for Creating Quizzes 📝✍️
Only the user tpye of 'teacher' has access to create and update quizzes. Currently, the quizzes are in the form of a `quizzes` table linking to a `quiz_questions` table with subject-specific questions. The teacher user can select on the 'Create new quiz' option in the teacher menu. They will then be prompted to enter a quiz name eg *Easy English*, and a new quiz will be added to the `quizzes` table in the `trivia_questions` database. The teacher can then add/delete questions in that quiz. 

### Instructions for Game Play 🕹️⌨️
To play the console game, simply follow the instructions in the prompt:
- for the `user_name` input, enter a string e.g. _Jane Doe_ 
- for the `Please enter your subject choice:` input, enter a number that corresponds to the subject selection you would like 
to make e.g. _3_
- for the `Please enter your answer choice A, B, C or D:` input, enter a letter that corresponds to the answer selection you would 
like to make e.g. _A_

> [!TIP] 
> Where prompted for letter/number input, you should only enter a letter/number that is in the provided list. Below are some input/output examples of use. 

**_Example Input:_**

If you want to select 'Math' from the list below then you would need to 
type **2** in the input section:
```
1. English
2. Math
3. History
4. Science
```
**_Example Output:_**
 
Enter your subject choice number: 2

Your selected subject is: 'Math'

**_Example Input (letters):_**

If you want to select 'Sad' from the list below then you would need to type **A** in the input section:
```
A. Sad
B. Excited
C. Joyful
D. Glad
```
**_Example Output:_**
 
Please enter the letter for your answer choice (A, B, C or D): A

Your selected answer is: 'Sad'

### How to use the Test Suite
The unit tests are in the `unit test files` folder and can be run by making sure all the imports are correct. There is a test file for each individual file used during the project, as seen below:
- test_app.py
- test_game.py
- test_main.py
- test_questions.py
- test_user.py

The tests were created using unittests in PyCharm, and are still undergoing further debugging and improvement.
