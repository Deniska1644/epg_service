from fastapi import APIRouter


router = APIRouter(
    # prefix='/'
)


@router.get('/list')
async def main():
    return {'status': 'ok'}
