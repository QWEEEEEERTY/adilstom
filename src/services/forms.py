from pydantic import BaseModel, Field, model_validator, ConfigDict
import datetime
from .validators import validate_date, validate_phone
from typing import Optional


class GetScheduleForm(BaseModel):
    start: str
    end: str | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode='after')
    def validate(self):
        self.start = validate_date(self.start)
        if self.end is None:
            self.end = self.start
        else:
            self.end = validate_date(self.end)
        return self


class CreateZapisForm(BaseModel):
    patientName: str = Field("ФИО пациента", min_length=1)
    iin: Optional[str] = ""
    phone: str = "+7(777)777-77-77"
    day: str = "30.11.2024"
    startHour: int = Field(ge=10, le=18)
    startMinute: int = Field(ge=0, lt=60)
    endHour: Optional[int] = Field(None, ge=10, le=18)
    endMinute: Optional[int] = Field(None, ge=0, lt=60)
    doctor: int = Field(ge=10_000, lt=100_000)
    comment: Optional[str] = ""
    zhaloba: Optional[str] = ""

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode='after')
    def validate(self):
        self.day = validate_date(self.day)
        self.phone = validate_phone(self.phone)

        start_time = datetime.datetime(2000, 1, 1, self.startHour, self.startMinute)
        end_time = start_time + datetime.timedelta(minutes=40)
        self.endHour = end_time.hour
        self.endMinute = end_time.minute

        self.comment = f"{self.comment}"
        return self


class DeleteZapisForm(BaseModel):
    date: str
    phone: str

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate(self):
        self.date = validate_date(self.date)
        self.phone = validate_phone(self.phone)
        return self
