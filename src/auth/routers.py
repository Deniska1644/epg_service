from fastapi import APIRouter


router = APIRouter(
    prefix='/clients'
)


@router.get('')
async def main():
    return {'status': 'ok'}
