import requests

def obtener_latitud_longitud(codigo_postal, pais='ES'):
    """
    Obtiene latitud y longitud a partir del código postal usando la API de OpenStreetMap (Nominatim).
    :param codigo_postal: Código postal a geocodificar.
    :param pais: País donde buscar el código postal (por defecto, España).
    :return: Diccionario con latitud y longitud o None si no se encontró.
    """
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'postalcode': codigo_postal,
        'country': pais,
        'format': 'json',
        'limit': 1  # Limita la respuesta a un solo resultado
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            return {
                'latitud': data[0]['lat'],
                'longitud': data[0]['lon']
            }
        else:
            return None
    else:
        return None