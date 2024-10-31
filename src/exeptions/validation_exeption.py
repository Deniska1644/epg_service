from fastapi.exceptions import HTTPException
from fastapi import status

user_sex_exeption = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="sex user must be male or female",
)

incorect_data_string = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="date must be YYYY-MM-DD",
)
