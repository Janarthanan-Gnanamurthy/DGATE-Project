from fastapi import FastAPI, Depends, Form, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from schema import Course as SchemaCourse,CourseResponse , Topics as SchemaTopics, Questions as SchemaQuestions, CourseWithTopics, TopicsWithTests, ResultsCreate, ResultsResponse, ResultsList,UserCreate, UserResponse, TestCreate, TestResponse
from models import Course, Topics, Questions, Results, User, Test

import os
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/course", response_model=SchemaCourse)
async def course(course: SchemaCourse):
    new_course = Course(code=course.code, title=course.title)
    db.session.add(new_course)
    db.session.commit()

    return new_course


@app.get("/course/{course_id}", response_model=CourseWithTopics)
async def get_course(course_id: int):
    course = db.session.query(Course).filter(Course.id == course_id).first()
    return course

@app.get("/courses", response_model=List[CourseResponse])
async def get_courses():
    courses = db.session.query(Course).all()
    return courses

@app.post("/topics", response_model=SchemaTopics)
def create_topic(topic: SchemaTopics):
    db_topic = Topics(title=topic.title, course_id=topic.course_id)
    db.session.add(db_topic)
    db.session.commit()
    return db_topic

@app.get("/topics/{topic_id}", response_model=TopicsWithTests)
def get_topic(topic_id: int):
    topic = db.session.query(Topics).filter(Topics.id == topic_id).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@app.post("/questions", response_model=SchemaQuestions)
def create_question(question: SchemaQuestions):
    db_question = Questions(**question.dict())
    db.session.add(db_question)
    db.session.commit()
    return db_question

@app.get("/questions/{question_id}", response_model=SchemaQuestions)
def get_question(question_id: int):
    question = db.session.query(Questions).filter(Questions.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.post('/results', response_model=ResultsCreate)
async def Create_results(request: Request):  #user_id: str = Form(...), topic_id: str = Form(...), score: float = Form(...), selected_options: dict = Form(...), metrics: dict = Form(...)
    form_data = await request.json()
    db_results = Results(
        user_id=form_data['user_id'],
        test_id=form_data['test_id'],
        score=form_data['score'],
        selected_options=form_data['selected_options'],
        metrics=form_data['metrics'],
    )
    db.session.add(db_results)
    db.session.commit()
    return db_results

@app.get('/result/{results_id}', response_model=ResultsResponse)
async def Get_results(results_id: int):
    result = db.session.query(Results).filter(Results.id==results_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Result Not Found")
    return result

@app.get('/results/{user_id}', response_model=List[ResultsList])
async def Get_results(user_id: int):
    results = db.session.query(Results).filter(Results.user_id==user_id).all()
    if results is None:
        raise HTTPException(status_code=404, detail="Results Not Found")
    return results


@app.post('/user', response_model=UserResponse)
def Create_user(user: UserCreate):
    db_user = User(**user.dict())
    db.session.add(db_user)
    db.session.commit()

    return db_user

@app.post('/test')
async def Create_test(test_data: TestCreate):
    topic = db.session.query(Topics).filter(Topics.id == test_data.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Create a new test
    new_test = Test(name=test_data.name, topic_id=test_data.topic_id)

    # Associate questions with the test
    for question_id in test_data.question_ids:
        question = db.session.query(Questions).filter(Questions.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found")
        new_test.questions.append(question)

    # Commit changes to the database
    db.session.add(new_test)
    db.session.commit()

    return 1

@app.get('/test/{id}', response_model=TestResponse)
def Get_test(id):
    test = db.session.query(Test).filter(Test.id == id ).first()

    return test

@app.put('/test/{id}', response_model=TestResponse)
def Update_test(id):
    test = db.session.query(Test).filter(Test.id == id ).first()

    test.submitted = True
    db.session.commit()

    return test

@app.post('/upload/{topic_id}')
async def handle_data(request: Request, topic_id):
    data = await request.json()

    questions = []
    for question_data in data:
        print(question_data)
        question = {
            'statement': question_data[1],
            'option_a': question_data[2],
            'option_b': question_data[3],
            'option_c': question_data[4],
            'option_d': question_data[5],
            'answer': question_data[6],
            'answer_uri': 'None',
            'explanation': question_data[7],
            'difficulty': 'Level 2',
            'topic_id': topic_id

        }
        questions.append(Questions(**question))

    for question in questions:
        db.session.add(question)
        db.session.commit()

    return {'message': questions}

# def save_question_to_db(question: Questions):
#     return -1
