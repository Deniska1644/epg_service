from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import re

from exeptions.validation_exeption import incorect_data_string, user_sex_exeption


class UserFilter(BaseModel):
    sex: str | None = None
    name: str | None = None
    last_name: str | None = None
    date_registration_from: datetime | str | None = None
    date_registration_to: datetime | str | None = None
    skip: int | None = None
    limit: int | None = None

    @field_validator('date_registration_from', 'date_registration_to')
    @classmethod
    def convert_date(cls, v) -> datetime:
        regular = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
        if v is not None:
            if not re.match(regular, v):
                raise incorect_data_string
            data_ = list(map(lambda x: int(x), v.split('-')))
            return datetime(*data_)
        return v

    @field_validator('sex')
    @classmethod
    def chec_sex(cls, v: str) -> str:
        if v is not None:
            if v.lower().strip() not in ['male', 'femail']:
                raise user_sex_exeption
            return v.lower().strip()
        return v
