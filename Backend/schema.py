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

class TopicCreate(BaseModel):
    title:str
    course_id: int

class TopicResponse(BaseModel):
    id :int

class Questions(BaseModel):
    id:int
    statement: str
    description: Optional[str] = None
    question_uri: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    answer: str
    answer_uri: Optional[str] = None
    explanation: str
    difficulty: str

    topic_id: int 

    class Config:
        orm_mode = True

class SelectQuestions(BaseModel):
    id: int
    statement: str

class ResultsCreate(BaseModel):
    user_id: int
    test_id: int
    score: float
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