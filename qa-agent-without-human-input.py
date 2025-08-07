import os
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

load_dotenv()

MODEL=os.getenv("MODEL")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

llm = LLM(model=MODEL,
          temperature=0,
          api_key=GROQ_API_KEY,
          )

# Define your agents with roles, goals, tools, and additional attributes
researcher = Agent(
    role='Expert {subject} Teacher & Question Designer',
    goal='Design accurate, level-appropriate, and conceptually diverse questions based on the given subject, quantity, and format.',
    backstory=(
        "You are a veteran educator with expertise in {subject}. You craft questions for exams, quizzes."
        "You align your questions with curriculum stanqadards and cognitive goals."
    ),
    verbose=True,
    llm=llm
)
writer = Agent(
    role='Expert {subject} Answering Agent',
    goal='Provide accurate, concise, and level-appropriate answers to the given set of questions.',
    backstory=(
        "You are an experienced subject matter expert who understands the nuances of {subject}. Your responsibility is to analyze each provided question carefully and return the correct answer."
        "You ensure clarity, correctness, and can optionally provide brief justifications or explanations for each answer depending on the question type."
    ),
    verbose=True,
    llm=llm
)

# Create tasks for your agents
task1 = Task(
    description=(
        "Generate {number_of_questions} questions on the topic: {subject}."
        "The questions should be level-appropriate for {level} learners. don't give answer of any question."
    ),
    expected_output="A list of {number_of_questions} well-structured and diverse questions on {subject} designed for {level} learners. Each question should be clearly stated and educationally valuable.",
    agent=researcher,
    output_file=os.path.join(os.getcwd(), "output", "{subject}.txt")
)

task2 = Task(
    description=(
        "Provide accurate answers for the given set of questions."
    ),
    expected_output='A list of answers to the provided questions in {subject}, optionally including explanations where necessary.',
    agent=writer,
    context=[task1],
    output_file=os.path.join(os.getcwd(), "output", "{subject}_answer.txt")
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer],
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
