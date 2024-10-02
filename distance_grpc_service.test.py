import unittest
from google.protobuf.json_format import MessageToJson
from distance_grpc_service import *
import json
import grpc


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


    def test_latitudeMayor90(self):
        result = test_valid_request(92, -70.5955963, 94, -71.5980458,"km")
        if self.assertRaises(ValueError):
            self.assertEqual(result["distance"], -1)
            self.assertEqual(result["unit"],"invalid")

    def test_latitudeMenor90(self):
        result = test_valid_request(-92, -70.5955963, -94, -71.5980458, "km")
        if self.assertRaises(ValueError):
            self.assertEqual(result["distance"], -1)
            self.assertEqual(result["unit"], "invalid")

    def test_valoresString(self):
        result = test_valid_request("0", "0", "0", "0","km")
        if self.assertRaises(ValueError):
            self.assertEqual(result["distance"], -1)
            self.assertEqual(result["unit"], "invalid")

    def test_defaultUnit(self):
        result = test_valid_request(70, 70, 70, 70,"")
        self.assertEqual(result["unit"], "km")

    def test_invalidUnit(self):
        result = test_valid_request(70, 70, 70, 70,"yd")
        with self.assertRaises(ValueError):
            pass

#prueba



if __name__ == '__main__':
    unittest.main()
