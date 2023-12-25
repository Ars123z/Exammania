import csv
from django.db import IntegrityError

from .models import Exam, ExamQuestion, ExamQuestionOptions

def upload_exam_data(file_path):
    """Uploads exam data from a CSV file to the Django database.

    Args:
        file_path: The path to the CSV file.
    """
    exam_name= 'jee_mains'
    exam_year= 2013

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            # Get the exam name and year.
            

            # Get the question body.
            question_body = row[0]
            question_answer = row[1]
            subject_value = row[2]
            difficulty_value = row[3]

            # Get the option contents.
            option_contents = row[4:8]
            correct = row[8:]
            print(correct)
            print(option_contents)

            # Check if the question exists.
            try:
                question = ExamQuestion.objects.get(body=question_body, answer=question_answer, subject=subject_value, difficulty_level=difficulty_value)
            except ExamQuestion.DoesNotExist:
                question = ExamQuestion(body=question_body, answer=question_answer, subject=subject_value, difficulty_level=difficulty_value)
                question.save()

            # Check if the options exist.
            options = []
            for option_content in option_contents:
                try:
                    option = ExamQuestionOptions.objects.get(content=option_content)
                    options.append(option)
                except ExamQuestionOptions.DoesNotExist:
                    option = ExamQuestionOptions(content=option_content)
                    option.save()
                    options.append(option)

            # Add the options to the question.
            question.options.set(options)

            # Set the correct options.
            correct_options_content = row[8:]
            
            correct_options = []
            for correct_option in correct_options_content:
                coption = ExamQuestionOptions.objects.get(content=correct_option)
                correct_options.append(coption)

            

            question.correct_options.set(correct_options)

            # Add the question to the exam.
            # exam = Exam(name=exam_name, year=exam_year)
            # exam.save()
            exam = Exam.objects.get(name=exam_name, year=exam_year)
            exam.questions.add(question)

            # Save the exam.
            

if __name__ == "__main__":
    # Get the path to the CSV file.
    file_path = "data/examdata/JeeMains/2013.csv"

    # Upload the exam data.
    upload_exam_data(file_path)
