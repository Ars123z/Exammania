import csv
from .models import BookQuestion, BookQuestionOption, Exercise

def populate_database(csv_file_path):
    exercise_name= "1(A)"
    exercise = Exercise.objects.get(name=exercise_name)
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
        # Get the exam name and year.
        

        # Get the question body.
            question_body = row[0]
            question_answer = row[1]
            difficulty_value = row[2]

            # Get the option contents.
            option_contents = row[3:7]
            correct = row[7:]
            print(correct)
            print(option_contents)

            try:
                question = BookQuestion.objects.get(body=question_body, answer=question_answer, difficulty_level=difficulty_value)
            except BookQuestion.DoesNotExist:
                question = BookQuestion(body=question_body, answer=question_answer, difficulty_level=difficulty_value)
                question.save()

            options = []
            for option_content in option_contents:
                try:
                    option = BookQuestionOption.objects.get(content=option_content)
                    options.append(option)
                except BookQuestionOption.DoesNotExist:
                    option = BookQuestionOption(content=option_content)
                    option.save()
                    options.append(option)

            # Add the options to the question.
            question.options.set(options)

            # Set the correct options.
            correct_options_content = row[7:]
            
            correct_options = []
            for correct_option in correct_options_content:
                coption = BookQuestionOption.objects.get(content=correct_option)
                correct_options.append(coption)

        

            question.correct_options.set(correct_options)
            exercise.questions.add(question)
            print(question_body)


if __name__ == "__main__":
    csv_file_path = "bookcsv.csv"
    populate_database(csv_file_path)