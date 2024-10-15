import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector

def parse_html(url, palabra_filtro, productos_totales_alcampo):
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

        productos = soup.find_all('div', class_='product-card-container')

        for producto in productos:
            nombre_producto = producto.find('h3', class_='_text_f6lbl_1 _text--m_f6lbl_23').get_text(strip=True)
            
            
            precios_div = producto.find('div', class_='price-pack-size-container')
            
            precio_rebajado_tag = precios_div.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1fkdssq-0 kVIDwa')

            if precio_rebajado_tag:
                precio_producto = precio_rebajado_tag.get_text(strip=True).strip()
                
            else :
                precio_producto = precios_div.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1fkdssq-0 eVdlkb').get_text(strip=True).strip()
                
            precios_kg_tag=producto.find('span',class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1vpsrpe-2 sc-bnzhts-0 cOeicp jIzHwa')

            if precios_kg_tag:
                precio_kg = precios_kg_tag.get_text().strip()
            else: 
                precio_kg = producto.find('span', class_ = '_text_f6lbl_1 _text--m_f6lbl_23 sc-1vpsrpe-2 sc-bnzhts-0 VJkMO jIzHwa').get_text(strip = True).strip()
            
            link_get = producto.find('div', class_ ='image-container').find('img')
            link_imagen = link_get['src'] if link_get else None
            nombre_supermercado = "alcampo"
            print (nombre_producto, precio_producto, precio_kg, link_imagen )
            productos_totales_alcampo.append({
                            'nombre' : nombre_producto,
                            'precio' : precio_producto,
                            'precio/kg' : precio_kg,
                            'imagen' : link_imagen, 
                            'supermercado' : nombre_supermercado })
                



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

def aceptar_cookies(driver):
    try:
        # Localizamos el botón de aceptar cookies usando el ID
        boton_cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')  
        boton_cookies.click()
        print("Cookies aceptadas.")
        time.sleep(2)  # Esperamos unos segundos para asegurarnos de que desaparece la ventana de cookies
    except Exception as e:
        print("No se encontró la ventana de cookies o ya fue aceptada.", e)

def hlml_carrefour(url_base, palabra_filtro, productos_totales_carrefour):
    try:
        
        
        offset = 0
        numero_paginas = 30
        for page in range(numero_paginas):
            chrome_options = Options()
            #chrome_options.add_argument("--headless")
            #chrome_options.add_argument("--disable-gpu")
            #chrome_options.add_argument("--no-sandbox")
            #chrome_options.add_argument("--disable-dev-shm-usage")
            #chrome_options.add_argument("--window-size=1920x1080")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            current_url = f"{url_base}?offset={offset}"
            driver.get(current_url)
            time.sleep(15)

            aceptar_cookies(driver)

            tiempo_maximo_scroll = 50
            tiempo_inicial = time.time()
            while (time.time() - tiempo_inicial)< tiempo_maximo_scroll:
                
                
                    
                # Desplazarse hacia abajo
                    
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(5)  # Esperar unos segundos para que carguen los nuevos productos

                print('scrolling')
                try:
                    # Esperar hasta que los productos estén presentes en el DOM
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card')),
                        EC.presence_of_element_located((By.XPATH, "//img[starts-with(@src, 'http')]"))

                    )

                    soup= BeautifulSoup(driver.page_source, 'html.parser')                  ## guardamos en la variable soup el contenido de la pagina
                
                    productos2 = soup.find_all('div', class_='product-card')          ## buscamos todos los productos de la pagina
                    for bucle in productos2:                ## recorremos los datos obtenidos de la lista de productos
                        nombre_producto = bucle.find('a', class_='product-card__title-link track-click').get_text(strip=True).lower().strip()## Separamos la etiqueta html para poder obtener solo el texto
                        print (nombre_producto)
                        precios_div = bucle.find('div', class_='product-card__prices')
                        precio_normal_tag = precios_div.find('span', class_='product-card__price--strikethrough')
                        precio_rebajado_tag = precios_div.find('span', class_='product-card__price--current')

                        if precio_rebajado_tag:
                            precio_producto = precio_rebajado_tag.get_text(strip=True).lower().strip()
                            print(precio_producto)
                        else :
                            precio_producto = precios_div.find('span', class_='product-card__price').get_text(strip=True).lower().strip()
                            print(precio_producto)
                        

                        precio_kg_div = bucle.find('div', class_='product-card__price-per-unit--container')
                        precio_kg_rebajado = precio_kg_div.find('span', class_= 'product-card__price-per-unit')
                        if precio_kg_rebajado:
                            precio_kg = precio_kg_rebajado.get_text(strip=True).lower().strip()
                            print(precio_kg)
                        else:
                            precios_div.find('div', class_='product-card__price')
                            print(precio_kg)
                        
                        nombre_supermercado = 'carrefour'
                        imagen_tag = bucle.find('a', class_='product-card__media-link track-click').find('img')
                        if imagen_tag:
                            link_imagen = imagen_tag.get('src', None)
                            
                            if link_imagen:
                                if link_imagen.startswith('http'):
                                    # Imagen normal con URL
                                    print(f"Link de la imagen: {link_imagen}")
                                    productos_totales_carrefour.append({
                                        'nombre' : nombre_producto,
                                        'precio' : precio_producto,
                                        'precio/kg' : precio_kg,
                                        'link_imagen' : link_imagen,
                                        'supermercado' : nombre_supermercado
                                
                                        })
                                elif link_imagen.startswith('data:image'):
                                    # Imagen es un marcador de posición temporal
                                    print("La imagen está en base64 (posiblemente no cargada completamente)")
                                else:
                                    print("Formato de imagen no reconocido.")


                               
                        
                               ## comparamos si la palabra que buscamos esta en el nombre del producto
                        
                            
                            
                except Exception as e:
                    print(f"Error en el scraping: {e}")     ## si esta la añadimos a la lista de productos totales
            numero_paginas= get_total_pages(soup)
            print(numero_paginas)
            offset = offset + 24
            time.sleep(2)           
            driver.quit() ## cerramos el navegador    
    except:
        print(f"error")

def html_eroski(url,palabra_filtro,productos_totales_eroski):
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
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.product-img'))
                    )
                except:
                    print("No se han encontrado más imágenes o ha habido un error.")
                    

            # Calcular nueva altura después de desplazarse
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Si no hay más contenido, salir del bucle
                last_height = new_height

            soup = BeautifulSoup(driver.page_source, 'html.parser')#guardamos el contenido de la pagina en la variable
            productos3 = soup.find_all('div', class_= 'col border-0 product-item-lineal item-type-1 product-with-picto col-xs-12 col-sm-12 col-md-6 col-lg-4')#selecciona directamente la etiqueta a de la clase h2 con la etiqueta a 
            
            for producto in productos3:

                nombre_producto = producto.find('h2', class_= 'product-title').find('a').get_text(strip =True)
                precio_producto = producto.find('span', class_= 'price-offer-now').get_text(strip=True)
                precio_por_kg = producto.find('span', class_= 'price-product')
                if precio_por_kg:
                    precio_por_kg = precio_por_kg.get_text(strip = True)
                else:
                    precio_por_kg = "no disponible"
                nombre_supermercado = 'eroski'

                link_tag = producto.find('img', class_='product-img')
                if link_tag:
                            link_imagen = link_tag.get('src', None)
                            
                            if link_imagen:
                                if link_imagen.startswith('http'):
                                    # Imagen normal con URL
                                    print(f"Link de la imagen: {link_imagen}")
                                    productos_totales_eroski.append({
                                        'nombre' : nombre_producto,
                                        'precio' : precio_producto,
                                        'precio/kg' : precio_por_kg,
                                        'link_imagen' : link_imagen,
                                        'supermercado' : nombre_supermercado
                                
                                        })
                                elif link_imagen.startswith('data:image'):
                                    # Imagen es un marcador de posición temporal
                                    print("La imagen está en base64 (posiblemente no cargada completamente)")
                                else:
                                    print("Formato de imagen no reconocido.")
                
                                # Cuando estamos buscando los productos, los comparamos con nombreproducto y si es el indicado, se guarda en la lista 


            driver.quit()
    except:
        print(f"error")


def analisis_supermercados(urls_alcampo, urls_carrefour, urls_eroski, palabra_filtro):
    productos_totales_alcampo = []
    productos_totales_carrefour = []
    productos_totales_eroski = []
    
    # Analizar Alcampo
    for url in urls_alcampo:
        print(f"\nAnalizando URL de Alcampo: {url}\n")
        parse_html(url, palabra_filtro, productos_totales_alcampo)
    
    productos_unicos_set_alcampo = set()
    productos_unicos_alcampo = []

    for producto in productos_totales_alcampo:
        # Convertir el diccionario en una tupla de tuplas (clave, valor)
        producto_tuple = tuple(sorted(producto.items()))  # ordenar para evitar problemas de orden

        # Agregar al conjunto solo si no está ya presente
        if producto_tuple not in productos_unicos_set_alcampo:
            productos_unicos_set_alcampo.add(producto_tuple)  # Añadir a set para controlar duplicados
            productos_unicos_alcampo.append(producto)  # Agregar el diccionario original a la lista de productos únicos

    #  Carrefour
    for url in urls_carrefour:
        print(f"\nAnalizando URL de Carrefour: {url}\n")
        hlml_carrefour(url, palabra_filtro, productos_totales_carrefour)
    
    productos_unicos_set_carrefour = set()
    productos_unicos_carrefour = []

    for producto in productos_totales_carrefour:
        # Convertir el diccionario en una tupla de tuplas (clave, valor)
        producto_tuple = tuple(sorted(producto.items()))

        # Agregar al conjunto solo si no está ya presente
        if producto_tuple not in productos_unicos_set_carrefour:
            productos_unicos_set_carrefour.add(producto_tuple)
            productos_unicos_carrefour.append(producto)

    #  Eroski
    
    for url in urls_eroski:
        print(f"\nAnalizando URL de Eroski: {url}\n")
        html_eroski(url, palabra_filtro, productos_totales_eroski)

    productos_unicos_set_eroski = set()
    productos_unicos_eroski = []

    for producto in productos_totales_eroski:
        # Convertir el diccionario en una tupla de tuplas (clave, valor)
        producto_tuple = tuple(sorted(producto.items()))

        # Agregar al conjunto solo si no está ya presente
        if producto_tuple not in productos_unicos_set_eroski:
            productos_unicos_set_eroski.add(producto_tuple)
            productos_unicos_eroski.append(producto)

    # Retornar los diccionarios o listas de productos únicos para cada supermercado
    return {
        'alcampo': productos_unicos_alcampo,
        'carrefour': productos_unicos_carrefour,
        'eroski': productos_unicos_eroski
    }

urls_a_analizar_alcampo= [
    "https://www.compraonline.alcampo.es/categories/frescos/OC2112?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/leche-huevos-l%C3%A1cteos-yogures-y-bebidas-vegetales/OC16?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/alimentaci%C3%B3n/OCC10?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/desayuno-y-merienda/OC10?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/congelados/OC200220183?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/comida-preparada/OC20022018?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/bebidas/OCC11?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/supermercado-ecol%C3%B3gico/OC26112021?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/sin-gluten-sin-lactosa-y-otras-dietas-espec%C3%ADficas/OCSINGSINL?source=navigation",
    #"https://www.compraonline.alcampo.es/categories/veganos/OC09112021?source=navigation",
]

urls_a_analizar_carrefour = [
    "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
   

    ]

urls_a_analizar_eroski = ["https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado/"
                          
                          ]

# Pedir la palabra de búsqueda
def conectar_mysql():
    db = mysql.connector.connect(
        host = '212.47.235.212',
        user = 'remoto',
        password = '1234',
        database = 'ISO'

    )
    return db

def vaciar_tabla(db, tabla):
    try:
        cursor = db.cursor()
        sql_delete = f"DELETE FROM {tabla}"
        cursor.execute(sql_delete)
        db.commit()
        print(f"Tabla {tabla} vaciada correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al vaciar la tabla {tabla}: {err}") 

def insertar_producto(db, producto):
    try:
        cursor = db.cursor()
       
        if producto['supermercado'] == 'alcampo':
            tabla = 'productos_alcampo'
        elif producto['supermercado'] == 'carrefour':
            tabla = 'productos_carrefour'
        elif producto['supermercado'] == 'eroski':
            tabla = 'productos_eroski'

        
        
        sql = f"""
        INSERT INTO {tabla} (nombre, precio, precio_por_kg, link_imagen, supermercado) 
        VALUES (%s, %s, %s, %s)
        """
        valores = (producto['nombre'], producto['precio'], producto.get('precio/kg', None), producto.get('imagen', None), producto['supermercado'])
        cursor.execute(sql, valores)
        db.commit()
        print(f"Producto '{producto['nombre']}' insertado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar el producto: {err}")
    


def almacenar_productos(productos_dict):
    conexion = conectar_mysql()
    if conexion:
        vaciar_tabla(conexion, 'productos_alcampo')
        vaciar_tabla(conexion, 'productos_carrefour')
        vaciar_tabla(conexion, 'productos_eroski')
        for supermercado, productos in productos_dict.items():
            for producto in productos:
                insertar_producto(conexion, producto)
        conexion.close()
    else:
        print("No se pudo conectar a la base de datos.")      
palabra = input("Seleccione el alimento que desea buscar: ")

# Ejecutar el análisis
productos_unicos = analisis_supermercados(urls_a_analizar_alcampo, urls_a_analizar_carrefour,urls_a_analizar_eroski,palabra)
almacenar_productos(productos_unicos)
#productos_filtrados = analisis_supermercados(urls_a_analizar_alcampo, urls_a_analizar_carrefour,urls_a_analizar_eroski , palabra)



# Mostrar los productos encontrados


