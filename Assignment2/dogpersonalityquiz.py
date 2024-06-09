import requests  # Import the requests module to make HTTP requests

# Mapping of breed names to API format
breed_mapping = {
    "Bulldog": "bulldog",
    "Chihuahua": "chihuahua",
    "Golden Retriever": "retriever",
    "German Shepherd": "germanshepherd",
    "Italian Greyhound": "greyhound",
    "Husky": "husky",
    "Labrador": "labrador",
    "Pug": "pug",
    "Cocker Spaniel": "spaniel",
    "Shih Tzu": "shihtzu"
}

# Function to fetch random dog images from Dog API
def fetch_random_dog_images(breed):
    # Fetches a random dog image from the Dog API for a given breed.
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'error':
        print(f"Error: {data['message']}")
        return None  # Return None if there is an error
    return data['message']

# Function to display quiz questions and get user responses
def run_personality_quiz(questions, choices):
    # Runs the personality quiz based on provided questions and choices.
    print("Personality Quiz:")
    responses = []
    for i, question in enumerate(questions):
        print_question_with_choices(i, question, choices[i])
        response = get_user_response(len(choices[i]))
        responses.append(response - 1)  # Convert to 0-based index
    return responses

# Function to print quiz question with choices
def print_question_with_choices(question_number, question, choices):
    # Prints a quiz question with corresponding choices.
    print(f"\nQuestion {question_number + 1}: {question}")
    for i, choice in enumerate(choices):
        print(f"{i + 1}. {choice}")

# Function to get user response for a question
def get_user_response(num_choices):
    # Gets the user's response for a quiz question.
    while True:
        try:
            response = int(input(f"Your choice (1-{num_choices}): "))
            if 1 <= response <= num_choices:
                return response
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to determine dog breed based on quiz responses
def determine_breed(responses, breed_traits):
    # Determines the suggested dog breed based on user responses.
    score = {}
    for breed, traits in breed_traits.items():
        score[breed] = sum((r == t for r, t in zip(responses, traits)))
    return max(score, key=score.get)  # Returns the breed with the highest matching score

# Read quiz data from text file
def read_quiz_data(file_path):
    # Reads quiz data from a text file.
    questions = []
    choices = []
    breed_traits = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_index = lines.index('# Questions\n') + 1
    end_index = lines.index('# Choices\n')
    questions = [line.strip() for line in lines[start_index:end_index] if line.strip()]

    start_index = end_index + 1
    end_index = lines.index('# Breed Traits\n')
    choices = [line.strip().split(', ') for line in lines[start_index:end_index] if line.strip()]

    start_index = end_index + 1
    for line in lines[start_index:]:
        if line.strip():
            breed, traits = line.strip().split(': ')
            breed_traits[breed] = [int(trait) for trait in traits.split(', ')]

    return questions, choices, breed_traits

def main():
    breeds = ["Bulldog", "Chihuahua", "Golden Retriever", "German Shepherd",
              "Italian Greyhound", "Husky", "Labrador", "Pug",
              "Cocker Spaniel", "Shih Tzu"]

    # Read quiz data
    questions, choices, breed_traits = read_quiz_data('quiz_data.txt')

    # Run personality quiz
    user_responses = run_personality_quiz(questions, choices)

    # Print user responses in 1-10 format
    print("\nQuiz Answers:")
    with open('quizresults.txt', 'a') as file:
        file.write("Quiz Answers:\n")
        for i, (question, response) in enumerate(zip(questions, user_responses)):
            print(f"{i + 1}. {question}: {choices[i][response]}")
            file.write(f"{i + 1}. {question}: {choices[i][response]}\n")

    # Determine suggested breed based on user responses
    suggested_breed = determine_breed(user_responses, breed_traits)

    # Fetch random dog image for the suggested breed
    image_url = fetch_random_dog_images(breed_mapping.get(suggested_breed))
    if image_url:
        print(f"\nBased on your answers, if you were a dog you would be a: {suggested_breed}")
        print(f"Check out this cute {suggested_breed}! {image_url}")
    else:
        print(f"\nBased on your answers, if you were a dog you would be a: {suggested_breed}")
        print("Unfortunately, we couldn't fetch an image for this breed.")

    # Append the outcome to the text file
    with open('quizresults.txt', 'a') as file:
        file.write(f"Suggested breed: {suggested_breed}\n")

if __name__ == "__main__":
    main()
    
