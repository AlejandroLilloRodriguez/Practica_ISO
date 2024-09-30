import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager

def parse_html(url, palabra_filtro, productos_totales):
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(7)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Desplazarse hacia abajo
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Esperar unos segundos para que carguen los nuevos productos

            # Calcular nueva altura después de desplazarse
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Si no hay más contenido, salir del bucle
            last_height = new_height



        soup= BeautifulSoup(driver.page_source, 'html.parser')

        productos = soup.find_all('h3', class_='_text_f6lbl_1 _text--m_f6lbl_23')

        for producto in productos:
            nombre_producto = producto.get_text(strip=True)
            if palabra_filtro.lower() in nombre_producto.lower():
                productos_totales.append(nombre_producto)
                



        driver.quit()
    except:
        print(f"error")

def get_total_pages(soup):
    """Extrae el número total de páginas desde el HTML."""
    pagination_div = soup.find('div', class_='pagination__main')
    if pagination_div:
        text = pagination_div.get_text(strip=True)
        total_pages = int(text.split('de')[-1].strip())  # Extraer el número después de "de"
        return total_pages
    return 1  



def hlml_carrefour(url_base, palabra_filtro, productos_totales):
    try:
        
        
        offset = 0
        numero_paginas = 30
        for page in range(numero_paginas):
            chrome_options = Options()
            ##chrome_options.add_argument("--headless")
            #chrome_options.add_argument("--disable-gpu")
            #chrome_options.add_argument("--no-sandbox")
            #chrome_options.add_argument("--disable-dev-shm-usage")
            #chrome_options.add_argument("--window-size=1920x1080")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            current_url = f"{url_base}?offset={offset}"
            driver.get(current_url)
            time.sleep(7)

        
            tiempo_maximo_scroll = 30
            tiempo_inicial = time.time()
            while (time.time() - tiempo_inicial)< tiempo_maximo_scroll:
                
                
                    
                # Desplazarse hacia abajo
                    
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(3)  # Esperar unos segundos para que carguen los nuevos productos

                

                soup= BeautifulSoup(driver.page_source, 'html.parser')                  ## guardamos en la variable soup el contenido de la pagina
                productos2 = soup.find_all('div', class_='product-card__detail')          ## buscamos todos los productos de la pagina
                for bucle in productos2:                ## recorremos los datos obtenidos de la lista de productos
                    nombre_producto = bucle.find('a', class_='product-card__title-link track-click').get_text(strip=True)## Separamos la etiqueta html para poder obtener solo el texto
                    nombre_producto = nombre_producto.lower().strip()
                    precio_producto = bucle.find('span', class_= 'product-card__price').get_text(strip=True)
                    precio_producto = precio_producto.lower().strip()
                    precio_kg = bucle.find('span', class_= 'product-card__price-per-unit').get_text(strip=True)
                    precio_kg = precio_kg.lower().strip()

                    print(nombre_producto, precio_kg, precio_producto)        
                    if palabra_filtro.lower() in nombre_producto.lower():       ## comparamos si la palabra que buscamos esta en el nombre del producto
                        productos_totales.append({
                            'nombre' : nombre_producto,
                            'precio' : precio_producto,
                            'precio/kg' : precio_kg
                        })      ## si esta la añadimos a la lista de productos totales
            numero_paginas= get_total_pages(soup)
            print(numero_paginas)
            offset = offset + 24
            time.sleep(2)           
            driver.quit() ## cerramos el navegador    
    except:
        print(f"error")

def html_eroski(url,palabra_filtro,productos_totales):
    try:
        chrome_options = Options()
        ##chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(7)
        while True: #este metodo sirve para cargar todos los datos de la url
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                
            # Desplazarse hacia abajo
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Esperar unos segundos para que carguen los nuevos productos

            # Calcular nueva altura después de desplazarse
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Si no hay más contenido, salir del bucle
                last_height = new_height
            soup = BeautifulSoup(driver.page_source, 'html.parser')#guardamos el contenido de la pagina en la variable
            productos3 = soup.select('h2.product-title a')#selecciona directamente la etiqueta a de la clase h2 con la etiqueta a 
            for producto in productos3:
                nombre_producto = producto.get_text(strip=True)
                if palabra_filtro.lower() in nombre_producto.lower():
                    productos_totales.append(nombre_producto)
                
                # Cuando estamos buscando los productos, los comparamos con nombreproducto y si es el indicado, se guarda en la lista 


            driver.quit()
    except:
        print(f"error")


def analisis_supermercados(urls_alcampo, urls_carrefour, urls_eroski, palabra_filtro):
    productos_totales = []
    
    # Analizar Alcampo
    
    for url in urls_alcampo:
        print(f"\nAnalizando URL de Alcampo: {url}\n")
        parse_html(url, palabra_filtro, productos_totales)
    
    # Analizar Carrefour
    for url in urls_carrefour:
        print(f"\nAnalizando URL de Carrefour: {url}\n")
        hlml_carrefour(url, palabra_filtro, productos_totales)
    
    for url in urls_eroski : 
       print(f"\nAnalizando URL de Eroski: {url}\n")
       html_eroski(url,palabra_filtro,productos_totales)
    productos_unicos = list(set(productos_totales))
    return productos_unicos
urls_a_analizar_alcampo= [
    "https://www.compraonline.alcampo.es/categories/frescos/OC2112?source=navigation",
    "https://www.compraonline.alcampo.es/categories/leche-huevos-l%C3%A1cteos-yogures-y-bebidas-vegetales/OC16?source=navigation",
    "https://www.compraonline.alcampo.es/categories/alimentaci%C3%B3n/OCC10?source=navigation",
    "https://www.compraonline.alcampo.es/categories/desayuno-y-merienda/OC10?source=navigation",
    "https://www.compraonline.alcampo.es/categories/congelados/OC200220183?source=navigation",
    "https://www.compraonline.alcampo.es/categories/comida-preparada/OC20022018?source=navigation",
    "https://www.compraonline.alcampo.es/categories/bebidas/OCC11?source=navigation",
    "https://www.compraonline.alcampo.es/categories/supermercado-ecol%C3%B3gico/OC26112021?source=navigation",
    "https://www.compraonline.alcampo.es/categories/sin-gluten-sin-lactosa-y-otras-dietas-espec%C3%ADficas/OCSINGSINL?source=navigation",
    "https://www.compraonline.alcampo.es/categories/veganos/OC09112021?source=navigation",
]

urls_a_analizar_carrefour = [
    "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c",
    "https://www.carrefour.es/supermercado/la-despensa/cat20001/c",
    "https://www.carrefour.es/supermercado/congelados/cat21449123/c",
    "https://www.carrefour.es/supermercado/congelados/cat21449123/c",
    "https://www.carrefour.es/supermercado/limpieza-y-hogar/cat20005/c",
    "https://www.carrefour.es/supermercado/perfumeria-e-higiene/cat20004/c",
    "https://www.carrefour.es/supermercado/bebe/cat20006/c",
    "https://www.carrefour.es/supermercado/mascotas/cat20007/c",
    "https://www.carrefour.es/supermercado/parafarmacia/cat20008/c"

    ]

urls_a_analizar_eroski = ["https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060067-aceitunas-y-encurtidos/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060015-conservas-de-pescado/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060001-conservas-vegetales/","https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060076-frutos-secos-patatas-y-snacks/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059807-leche-batidos-y-bebidas-vegetales/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060029-legumbres-arroz-y-pasta/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059851-mantequilla-nata-y-cremas/","https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060042-platos-preparados/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059831-postres-lacteos-/","https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/5000365-productos-de-dietetica/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/5000364-productos-ecologicos/","https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060056-salsas-y-especias/",
                          "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059818-yogures/","https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/4000017-comida-internacional/",
                          "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059746-carnes-y-aves/","https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059880-curados-y-embutidos/",
                          "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059872-fiambres-y-cocidos/","https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059699-frutas/",
                          "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059760-huevos/","https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059894-ibericos/",
                          "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059736-mariscos/","https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059783-panaderia-y-pasteleria/",
                          "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059722-pescados/","https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059769-platos-preparados/",
                          "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059858-queso-y-membrillo/","https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059901-salchichas-pates-y-foie/",
                          "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059710-verduras-y-hortalizas/","",
                          "https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060119-la-tienda-del-cafe/","https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060182-azucar-y-edulcorante/",
                          "https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060162-bolleria/","https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060129-cacao-en-polvo-y-crema-de-cacao/",
                          "https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060202-caramelos-chicles-y-golosinas/","https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/5000189-cereales-y-barritas/",
                          "https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060190-chocolates-y-bombones/","https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060135-galletas/",
                          "https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/4000095-infusiones/","https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060173-miel-y-mermelada/",
                          "https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/2060149-pan-de-molde-y-tostado/","https://supermercado.eroski.es/es/supermercado/2060118-dulces-y-desayuno/5000302-productos-ecologicos/",
                          "https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060212-agua/","https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060304-cavachampan-y-sidra/",
                          "https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060233-cervezas/","https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060294-finos-dulces-y-aperitivos/",
                          "https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060315-licor/","https://supermercado.eroski.es/es/supermercado/2060211-bebidas/5000308-productos-ecologicos/",
                          "https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060219-refrescos/","https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060266-vinos-blancos/",
                          "https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060289-vinos-de-mesa-y-sangrias/","https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060278-vinos-rosados/",
                          "https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060252-vinos-tintos/","https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060243-zumos-y-nectar/",
                          "https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059952-helados-y-postres/","https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059983-panaderia-y-pasteleria/",
                          "https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059942-patatas-verduras-y-setas/","https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059927-pescado/",
                          "https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059920-pizzas/","https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059964-platos-preparados/",
                          "https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059934-marisco/","https://supermercado.eroski.es/es/supermercado/2059919-congelados/2059977-salteados-y-revueltos/",
                          ]
# Pedir la palabra de búsqueda
palabra = input("Seleccione el alimento que desea buscar: ")

# Ejecutar el análisis
productos_filtrados = analisis_supermercados(urls_a_analizar_alcampo, urls_a_analizar_carrefour,urls_a_analizar_eroski , palabra)



# Mostrar los productos encontrados
print("\nProductos encontrados:")
for producto in productos_filtrados:
    print(producto)

