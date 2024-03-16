from fastapi import FastAPI, Depends, Form, Request, HTTPException, status, Header
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from routers import auth

from schema import Course as SchemaCourse,CourseResponse , Topics as SchemaTopics, Questions as SchemaQuestions, CourseWithTopics, TopicsWithTests, TopicResponse,TopicCreate, ResultsCreate, ResultsResponse, ResultsList,UserCreate, UserResponse, TestCreate, TestResponse, SelectQuestions
from models import Course, Topics, Questions, Results, User, Test

import os
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID  #
from keycloak.exceptions import KeycloakGetError

# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="fastapi",
                                 realm_name="Myrealm",
                                 client_secret_key="ELpqaD95xNSOVXnEfK9JR37RvWHxdKy5")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=keycloak_openid.well_known()['token_endpoint'])

load_dotenv('.env')


app = FastAPI()

origins = [
    "http://localhost:5173",
]


app.include_router(auth.router)
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper function to validate and get user information from the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        token_info = keycloak_openid.introspect(token)
        username = token_info['name']
        
        return token_info
    except KeycloakGetError as e:
        if e.response_code == 403:
            raise HTTPException(
                status_code=403, detail="Invalid authentication credentials")
        else:
            raise HTTPException(
                status_code=500, detail="Error getting user information")

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    # return {"message": f"Hello, {user}!"}
    return user


@app.get("/")
async def root(current_user: dict = Depends(get_current_user)):
    username = current_user.get("preferred_username")
    roles = current_user.get("realm_access", {}).get("roles", [])
    return {"message": f"Welcome, {username}! You have the following roles: {roles}"}

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
