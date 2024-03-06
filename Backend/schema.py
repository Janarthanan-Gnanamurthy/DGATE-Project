from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    number: int
    password: str
    department: Optional[str] = None

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True

class Course(BaseModel):
    code: str
    title: str

    class Config:
        orm_mode = True

class CourseResponse(Course):
    id: int

class Topics(BaseModel):
    id: int
    title: str
    course_id: int

    class Config:
        orm_mode= True

class Questions(BaseModel):
    id:int
    statement: str
    description: str
    question_uri: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    answer: str
    answer_uri: str
    explanation: str
    difficulty: str

    topic_id: int 

    class Config:
        orm_mode = True

class ResultsCreate(BaseModel):
    user_id: int
    test_id: int
    score: int
    selected_options: dict
    metrics: Optional[dict] = None

class TestCreate(BaseModel):
    topic_id: int
    name: str
    question_ids: List[int]

    class Config:
        orm_mode = True

class TestID(BaseModel):
    id: int
    name: str

class TestResponse(BaseModel):
    id: int
    name: str
    submitted: bool
    parameters: Optional[dict] = None
    topic_id: int
    questions: List[Questions] = []

class ResultsResponse(ResultsCreate):
    id: int
    test: TestResponse

    class Config:
        orm_mode = True

class ResultsList(BaseModel):
    id: int
    test_id: int
    score: float
    metrics: Optional[dict] = None

class TopicsWithTests(Topics):
    test: List[TestID] = []

class CourseWithTopics(Course):
    topics: List[TopicsWithTests] = []