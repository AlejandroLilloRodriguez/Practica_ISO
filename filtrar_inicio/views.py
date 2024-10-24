from django.shortcuts import render

# Create your views here.
from buscador.models import ProductoTablaAlcampo, ProductoTablaCarrefour, ProductoTablaEroski

PALABRAS_CLAVE = {
    'aceite': ['aceite'],
    'carniceria': ['cerdo', 'vacuno', 'vaca', 'cordero', 'salchicha', 'chorizo', 'pollo'],
    'bebidas': ['cerveza', 'vino', 'agua', 'refresco', 'zumo', 'leche', 'café', 'infusión'],
    'pasta': ['pasta', 'macarrones', 'espaguetis', 'fideos', 'lasaña'],
    'lacteos': ['leche', 'queso', 'yogur', 'mantequilla', 'nata'],
    'frutos_secos': [
        'nuez', 'almendra', 'avellana', 'cacahuete', 'pistacho', 'anacardo', 'piñón', 'castaña', 
        'macadamia', 'pepita', 'pipa'
    ],
    'frutas_y_verduras': [
        'manzana', 'pera', 'plátano', 'naranja', 'mandarina', 'limón', 'pomelo', 'uva', 'fresa', 
        'cereza', 'melocotón', 'albaricoque', 'ciruela', 'kiwi', 'mango', 'papaya', 'piña', 'sandía', 
        'melón', 'frambuesa', 'arándano', 'mora', 'granada', 'aguacate', 'tomate', 'pepino', 'pimiento', 
        'zanahoria', 'calabacín', 'berenjena', 'lechuga', 'espinaca', 'acelga', 'col', 'coliflor', 
        'brócoli', 'repollo', 'apio', 'cebolla', 'ajo', 'puerro', 'patata', 'boniato', 'rábano', 'nabos', 
        'remolacha', 'alcachofa', 'espárrago', 'guisante', 'judía verde', 'habas', 'seta', 'champiñón'
    ],
    'arroz_y_legumbres': [
        'arroz', 'lenteja', 'garbanzo', 'judía', 'alubia', 'frijol', 'soja', 'habichuela', 'guisante', 'chícharo', 'haba', 'cuscús', 'quinoa', 'mijo', 'trigo sarraceno', 'amaranto'
    ],
    'pescados_y_mariscos': [
        'salmón', 'atún', 'bacalao', 'merluza', 'sardina', 'trucha', 'lenguado', 'dorada', 'lubina', 
        'gamba', 'langostino', 'camarón', 'cangrejo', 'mejillón', 'almeja', 'ostra', 'calamar', 'sepia', 
        'pulpo', 'bogavante', 'langosta', 'caracol de mar', 'erizo de mar'
    ],
    'panes_y_cereales': [
        'pan', 'cereales', 'galleta', 'bizcocho', 'tarta', 'croissant', 'bollo', 'magdalena', 'rosquilla', 'donut', 'churro', 'tostada', 'biscote', 'panecillo', 'panettone', 'pan dulce', 'pan de molde', 'pan de centeno', 'pan de espelta', 'pan de maíz', 'pan de avena', 'pan de cebada', 'pan de trigo'
    ]
    
}
def filtrar_productos(request, categoria):
    # Obtener las palabras clave para la categoría seleccionada
    palabras_clave = PALABRAS_CLAVE.get(categoria, [])
    
    # Buscar productos que coincidan con las palabras clave en las tres tablas
    productos_alcampo = ProductoTablaAlcampo.objects.filter(nombre__icontains=palabras_clave[0])
    for palabra in palabras_clave[1:]:
        productos_alcampo = productos_alcampo | ProductoTablaAlcampo.objects.filter(nombre__icontains=palabra)

    productos_carrefour = ProductoTablaCarrefour.objects.filter(nombre__icontains=palabras_clave[0])
    for palabra in palabras_clave[1:]:
        productos_carrefour = productos_carrefour | ProductoTablaCarrefour.objects.filter(nombre__icontains=palabra)

    productos_eroski = ProductoTablaEroski.objects.filter(nombre__icontains=palabras_clave[0])
    for palabra in palabras_clave[1:]:
        productos_eroski = productos_eroski | ProductoTablaEroski.objects.filter(nombre__icontains=palabra)

    # Unir todos los productos en una lista
    productos = list(productos_alcampo) + list(productos_carrefour) + list(productos_eroski)

    # Renderizar la plantilla con los productos filtrados
    return render(request, 'resultados_busqueda.html', {
        'productos': productos,
        'supermercado': None,
        'query': categoria
    })