import unittest
from geo_location import *

class TestGeo_location(unittest.TestCase):


    def test_latitudMayor90(self):
        with self.assertRaises(ValueError):
            Position(91, 0, 0)


    def test_latitudMenor90(self):
        with self.assertRaises(ValueError):
            Position(-91,0,0)

    def test_longitudMayor180(self):
        with self.assertRaises(ValueError):
            Position(0,181,0)

    def test_lngitudMenor180(self):
        with self.assertRaises(ValueError):
            Position(0,-181,0)

    def test_valoresString(self):
        with self.assertRaises(TypeError):
            Position("75","75",0)

if __name__ == '__main__':
    unittest.main()
