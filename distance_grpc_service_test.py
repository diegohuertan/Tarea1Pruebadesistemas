import unittest
from google.protobuf.json_format import MessageToJson
from distance_grpc_service import *
import json
import grpc
from distanceserviceORS import *

def test_valid_request(sourcelat, sourcelon, destinationlat, destinationlon, unit):

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.DistanceServiceStub(channel)

        message = pb2.SourceDest(
            source=pb2.Position(
                latitude=sourcelat, longitude=sourcelon
            ),
            destination=pb2.Position(
                latitude=destinationlat, longitude=destinationlon
            ),
            unit=unit
        )

        print(f"Message sent:\n{MessageToJson(message)}\n")

        response = stub.geodesic_distance(message)

        try:
            return json.loads(MessageToJson(response))
        except KeyError:
            print("One or more keys are missing!")


class TestDistance(unittest.TestCase):

    def test_defaultUnit(self):
        result = test_valid_request(70, 70, 70, 70,"")
        self.assertEqual(result["unit"], "km")

    def test_errorCatch(self):
        result=test_valid_request(91,181,91,181,"")
        self.assertEqual(result["unit"],"invalid")
        self.assertEqual(result["distance"],-1.0)


    def test_invalidUnit(self):
        result = test_valid_request(80, 80, 80, 80,"yd")
        self.assertEqual(result["unit"], "invalid")

    def test_distanceDelta02berlin(self):
        result = test_valid_request(13.38886, 52.51704, 13.39784, 52.50931,"km")
        API_KEY = '5b3ce3597851110001cf624898b34a01a6994f7899837fe3eb028422'
        distance_service = DistanceServiceORS(API_KEY)

        # Coordenadas en Berlín
        start = (13.38886, 52.51704)  # Brandenburg Gate
        end = (13.39784, 52.50931)  # Checkpoint Charlie

        distanceORS = distance_service.calculate_distance(start, end)
        margen_error = 0.2
        self.assertAlmostEquals(result["distance"], distanceORS, delta=margen_error )

    def test_distanceDelta01Berlin(self):
        result = test_valid_request(13.38886, 52.51704, 13.39784, 52.50931,"km")
        API_KEY = '5b3ce3597851110001cf624898b34a01a6994f7899837fe3eb028422'
        distance_service = DistanceServiceORS(API_KEY)

        # Coordenadas en Berlín
        start = (13.38886, 52.51704)  # Brandenburg Gate
        end = (13.39784, 52.50931)  # Checkpoint Charlie

        distanceORS = distance_service.calculate_distance(start, end)
        margen_error = 0.1
        self.assertAlmostEquals(result["distance"], distanceORS, delta=margen_error )

    def test_distanceDelta01randomvalues(self):
        result = test_valid_request(10.8,50.52,10.52,52.52,"km")
        API_KEY = '5b3ce3597851110001cf624898b34a01a6994f7899837fe3eb028422'
        distance_service = DistanceServiceORS(API_KEY)
        start = (10.8,50.52)
        end = (10.52,52.52)
        distanceORS = distance_service.calculate_distance(start, end)
        margen_error = 0.2
        self.assertAlmostEquals(result["distance"], distanceORS, delta=margen_error )




if __name__ == '__main__':
    unittest.main()
