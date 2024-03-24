from csv import reader
from datetime import datetime
from typing import Union

from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.aggregated_parking_data import AggregatedParkingData
from domain.parking import Parking
import config
import logging


logging.basicConfig(filename='parking_data.log', level=logging.INFO)

class FileDatasource:
    def __init__(
            self,
            accelerometer_filename: str,
            gps_filename: str,
            parking_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.open_accelerometer_file = None
        self.open_gps_file = None
        self.open_parking_file = None

    def read(self, sensorType) -> Union[AggregatedData, AggregatedParkingData]:
        """Метод повертає дані отримані з датчиків"""
        if sensorType=="basic":
            accelerometer_data = self.read_accelerometer_data()
            gps_data = self.read_gps_data()
            return AggregatedData(
                accelerometer_data,
                gps_data,
                datetime.now(),
                config.USER_ID,
            )
        if sensorType=="parking":
            parking_data = self.read_parking_data()
            return AggregatedParkingData(
                parking_data,
                datetime.now(),
                config.USER_ID,
            )



    def startReading(self):
        """Method should be called before starting to read data"""
        try:
            self.open_accelerometer_file = open(self.accelerometer_filename, "r")
            self.open_gps_file = open(self.gps_filename, "r")
            self.open_parking_file = open(self.parking_filename, "r")

            next(self.open_accelerometer_file)
            next(self.open_gps_file)
            next(self.open_parking_file)
        except FileNotFoundError:
            print("File not found. Please check the file paths.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        try:
            if self.open_accelerometer_file:
                self.open_accelerometer_file.close()

            if self.open_gps_file:
                self.open_gps_file.close()

            if self.open_parking_file:
                self.open_parking_file.close()

        except Exception as e:
            print(f"An error occurred while closing files: {e}")

    def read_accelerometer_data(self):
        try:
            row = next(reader(self.open_accelerometer_file))
            return Accelerometer(*map(float, row))
        except StopIteration:
            print('eof')

    def read_gps_data(self):
        try:
            row = next(reader(self.open_gps_file))
            return Gps(*map(float, row))
        except StopIteration:
            print('eof')

    def read_parking_data(self):
        try:
            row = next(reader(self.open_parking_file))
            empty_count, latitude, longitude = map(float, row)
            gps = Gps(latitude, longitude)
            parking_data = Parking(int(empty_count), gps)
            # log the data  docker exec -it container id /bin/bash
            # cat parking_data.log
            logging.info(parking_data)
            return Parking(empty_count, gps)
        except StopIteration:
            print('eof')

