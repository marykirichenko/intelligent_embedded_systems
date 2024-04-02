from datetime import datetime
import random
from pydantic import BaseModel, field_validator


class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class ParkingData(BaseModel):
    empty_count: float


class AgentData(BaseModel):
    accelerometer: AccelerometerData
    gps: GpsData
    parking: ParkingData
    timestamp: datetime
    user_id: int

    @classmethod
    @field_validator("user_id", mode="before")
    def set_user_id(cls):
        return random.randint(1, 10000)

    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, value):
        # Convert the timestamp to a datetime object
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            )