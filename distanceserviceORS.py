import openrouteservice
from openrouteservice.exceptions import ApiError

class DistanceServiceORS:
    def __init__(self, api_key):
        self.client = openrouteservice.Client(key=api_key)

    def calculate_distance(self, start, end, profile='foot-walking', radius=500):
        try:
            route = self.client.directions(
                coordinates=[start, end],
                profile=profile,
                format='geojson',
                radiuses=[radius, radius]
            )

            distance = route['features'][0]['properties']['segments'][0]['distance']
            return distance / 1000  # Convert to kilometers

        except ApiError as e:
            print(f"Error en la API: {e}")
            return None
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return None

# Uso de la clase
if __name__ == "__main__":
    API_KEY = '5b3ce3597851110001cf624898b34a01a6994f7899837fe3eb028422'
    distance_service = DistanceServiceORS(API_KEY)

    # Coordenadas en Berlín
    start = (13.38886, 52.51704)  # Brandenburg Gate
    end = (13.39784, 52.50931)    # Checkpoint Charlie

    distance = distance_service.calculate_distance(start, end)
    if distance is not None:
        print(f"La distancia entre los dos puntos es: {distance:.2f} km")