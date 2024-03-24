from dataclasses import dataclass

from datetime import datetime
from domain.parking import Parking


@dataclass
class AggregatedParkingData:
    parking: Parking
    timestamp: datetime
    user_id: int
