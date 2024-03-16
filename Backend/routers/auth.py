from fastapi import APIRouter

router = APIRouter(tags=['Auth'])

@router.get('/hmmm')
def hmmm():
  return {'this is auth.py'}