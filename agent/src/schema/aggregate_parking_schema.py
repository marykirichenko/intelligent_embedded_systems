from marshmallow import Schema, fields
from schema.parking_schema import ParkingSchema

class AggregatedParkingDataSchema(Schema):
    parking = fields.Nested(ParkingSchema)
    timestamp = fields.DateTime("iso")
    user_id = fields.Int()

