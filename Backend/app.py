from fastapi import FastAPI, Depends, Form, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from schema import Course as SchemaCourse,CourseResponse , Topics as SchemaTopics, Questions as SchemaQuestions, CourseWithTopics, TopicsWithTests, TopicResponse,TopicCreate, ResultsCreate, ResultsResponse, ResultsList,UserCreate, UserResponse, TestCreate, TestResponse, SelectQuestions
from models import Course, Topics, Questions, Results, User, Test

import os
from dotenv import load_dotenv

from keycloak import KeycloakOpenID
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="fastapi",
                                 realm_name="Myrealm",
                                 client_secret_key="ELpqaD95xNSOVXnEfK9JR37RvWHxdKy5")


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

userinfo = keycloak_openid.userinfo('eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJEVFdoYi01V2tSQWNUeWZaNFFQRTJXVEF6WnVzVUdRTDFpTTFmLUNnN0ljIn0.eyJleHAiOjE3MTA1NjI5NzksImlhdCI6MTcxMDU2MjY3OSwiYXV0aF90aW1lIjoxNzEwNTYyNjc5LCJqdGkiOiJiZGI0ODcxMS0yOTIxLTQ4NWItOGYzNy0yNzE2NmVjODJhOTYiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvcmVhbG1zL015cmVhbG0iLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiODM2Y2Q1ZTQtMTNlMy00NzdlLWFkNDItMTkwMDJhODk1ZGZlIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibXljbGllbnQiLCJub25jZSI6ImJkZDBlMGM4LWY0NDktNDc4OC04N2U4LTg0NzIzNzYzMWI5MSIsInNlc3Npb25fc3RhdGUiOiI0NjI0YmY3OC1lYjIxLTQ0MGYtYWM1My03MDk3ZDU2OTZmYzYiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly9sb2NhbGhvc3Q6NTE3MyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1teXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsIlN0dWRlbnQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiNDYyNGJmNzgtZWIyMS00NDBmLWFjNTMtNzA5N2Q1Njk2ZmM2IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiQmFsYWppIGt1bWFyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYmFsYWppIiwiZ2l2ZW5fbmFtZSI6IkJhbGFqaSIsImZhbWlseV9uYW1lIjoia3VtYXIiLCJlbWFpbCI6ImJhbGFqaUBtYWlsLmNvbSJ9.jX6Mn8JAb7bwgm9QQqVnKofgN8LOJsmNImL0LAwGqqpuxHsJREr2QAhPgdrFJA2LUZURtlJfpdxZx-NjHfVP0VPkyYAyQqhO1-Q_fw-WVlV0ZDjWMqsmDd1AG3xZa0F4E33P4WsB9U_sjX9nk3YEEpb6N05LxIYau9wcD257QkV-HsfK5gfsh3kCwnLQxrneJjjSp7t-NhjdlIzAMvzT-4_DjC0pP1OjtLFCjYBdpzMJ17C-71hOp7u9DvS9kJyIsyP0BF2iZv_Uy-xzApqO9X0Wf8h62Kzj-y4LvcYHJtX_uW8ty8j-1b22hkOYXL7vVOI4QpvPkIkFN6Wh2k40zA')
print(userinfo)

@app.get("/")
async def root():
    return {"message": user}

@app.post("/course", response_model=CourseResponse)
async def course(course: SchemaCourse):
    new_course = Course(**course.dict())
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

@app.post("/topics" , response_model=TopicResponse)
def create_topic(topic: TopicCreate):
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

@app.get("/select-questions/{topic_id}", response_model=List[SelectQuestions])
def create_question(topic_id):
    db_questions = db.session.query(Questions).filter(Questions.topic_id == topic_id).all()

    return db_questions

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
        question = {
            'statement': question_data[1],
            'option_a': question_data[2],
            'option_b': question_data[3],
            'option_c': question_data[4],
            'option_d': question_data[5],
            'answer': question_data[6],
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
