import json
import os
from crewai import Agent, Task, Crew, LLM, TaskOutput
from dotenv import load_dotenv
from typing import Tuple, Any

load_dotenv()
os.makedirs('output', exist_ok=True)

MODEL=os.getenv("MODEL")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

llm = LLM(model=MODEL,
          temperature=0,
          api_key=GROQ_API_KEY,
          )

# Define your agents with roles, goals, tools, and additional attributes
question_designer = Agent(
    role='Expert {subject} Teacher & Question Designer',
    goal='Design accurate, level-appropriate, and conceptually diverse questions based on the given subject, quantity, and format.',
    backstory=(
        "You are a veteran educator with expertise in {subject}. You craft questions for exams, quizzes."
        "You align your questions with curriculum standards and cognitive goals."
    ),
    verbose=True,
    llm=llm
)
answering_expert = Agent(
    role='Expert {subject} Answering Agent',
    goal='Provide accurate, concise, and level-appropriate answers to the given set of questions.',
    backstory=(
        "You are an experienced subject matter expert who understands the nuances of {subject}. Your responsibility is to analyze each provided question carefully and return the correct answer."
        "You ensure clarity, correctness, and can optionally provide brief justifications or explanations for each answer depending on the question type."
    ),
    verbose=True,
    llm=llm
)

def validate_question_content(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate question content meets requirements."""
    try:
        data = json.loads(result.raw)
        if not isinstance(data, list):
            print("Question content must be a list of strings.")
            return (False, "Question content must be a list of strings.")
        return (True, result)
    except Exception as e:
        return (False, str(e))

# Create tasks for your agents
task1 = Task(
    description=(
        "Generate {number_of_questions} questions on the topic: {subject}."
        "The questions should be level-appropriate for {level} learners. don't give answer of any question."
    ),
    expected_output="A list of json format with key:value or string. if there us is any MCQ question then key question and options."
                    "Format should be {question: 'what is python'}, and for MCQs [{'question': 'select one', "
                    "'options': {'a': 'select a', 'b': 'select b', 'c': 'select c', 'd': 'select d'}}]",
    agent=question_designer,
    output_file=os.path.join(os.getcwd(), "output", "{subject}.txt"),
    guardrail=validate_question_content,
    max_retries=1,
)

task2 = Task(
    description=(
        "Provide accurate answers for the given set of questions."
    ),
    expected_output='A list of answers to the provided questions in format.'
                    '{what is question: answer of that question} like {"what is 1+1": "2"}',
    agent=answering_expert,
    context=[task1],
    output_file=os.path.join(os.getcwd(), "output", "{subject}_answer.txt")
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[question_designer, answering_expert],
    tasks=[task1, task2],
    verbose=True,
)

# Get your crew to work!
result = crew.kickoff(inputs={
        'number_of_questions': '5',
        'subject': "python",
        'level': "5th class"
    })

print("######################")
print(result)
