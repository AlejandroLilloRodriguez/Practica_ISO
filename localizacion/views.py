from django.http import JsonResponse
import json
from geopy.geocoders import Nominatim
from django.shortcuts import render

def supermercados_cercanos(request):
    if request.method == "GET":
        return render(request, 'supermercados_cercanos.html')
    if request.method == "POST":
        try:
            # Leer datos JSON enviados
            body = json.loads(request.body)
            direccion = body.get("direccion")
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({"success": False, "message": "Datos mal formateados o dirección no proporcionada."}, status=400)

        # Verificar que la dirección no esté vacía
        if not direccion:
            return JsonResponse({"success": False, "message": "Dirección no proporcionada."}, status=400)

        # Usar geopy para obtener las coordenadas
        try:
            geolocator = Nominatim(user_agent="supermercados_app")
            location = geolocator.geocode(direccion)

            if location:
                return JsonResponse({
                    "success": True,
                    "lat": location.latitude,
                    "lon": location.longitude,
                })
            else:
                return JsonResponse({"success": False, "message": "No se encontraron coordenadas para la dirección proporcionada."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error al obtener las coordenadas: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)
