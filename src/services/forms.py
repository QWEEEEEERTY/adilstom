from typing_extensions import Self

from pydantic import BaseModel, Field, model_validator, ConfigDict, field_validator
import datetime
from typing import Optional, Any

from .validators import validate_date, validate_phone, validate_iin


class Form(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GetScheduleForm(Form):
    start: str
    end: str | None = None

    @model_validator(mode='after')
    def validate(self):
        self.start = validate_date(self.start)
        if self.end is None:
            self.end = self.start
        else:
            self.end = validate_date(self.end)
        return self


class TransferZapisForm(Form):
    phone: str = "+7(777)777-77-77"
    day: str = "30.11.2024"
    startHour: int = Field(ge=10, le=18)
    startMinute: int = Field(ge=0, lt=60)
    doctor: int = Field(ge=10_000, lt=100_000)
    endHour: Optional[int] = Field(None, ge=10, le=18)
    endMinute: Optional[int] = Field(None, ge=0, lt=60)

    @field_validator('day')
    def validate_day(cls, day: str):
        return validate_date(day)

    @field_validator('phone')
    def validate_phone(cls, phone: str):
        return validate_phone(phone)

    @model_validator(mode='after')
    def validate(self):
        start_time = datetime.datetime(2000, 1, 1, self.startHour, self.startMinute)
        end_time = start_time + datetime.timedelta(minutes=40)
        self.endHour = end_time.hour
        self.endMinute = end_time.minute
        return self


class CreateZapisForm(TransferZapisForm):
    patientName: str = Field("ФИО пациента", min_length=1)
    iin: str = Field(min_length=12, max_length=12)
    comment: Optional[str] = ""
    zhaloba: Optional[str] = ""

    @field_validator('iin')
    def validate_iin(cls, iin: str):
        return validate_iin(iin)


class DeleteZapisForm(Form):
    phone: str

    @model_validator(mode="after")
    def validate(self):
        self.phone = validate_phone(self.phone)
        return self
