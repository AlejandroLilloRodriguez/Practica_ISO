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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")
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

def hlml_carrefour(url, palabra_filtro, productos_totales):
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

    
       
        while True:
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

            soup= BeautifulSoup(driver.page_source, 'html.parser')                  ## guardamos en la variable soup el contenido de la pagina
            productos2 = soup.find_all('a', class_='product-card__title-link track-click')          ## buscamos todos los productos de la pagina
            for bucle in productos2:                ## recorremos los datos obtenidos de la lista de productos
                nombre_producto = bucle.get_text(strip=True)        ## Separamos la etiqueta html para poder obtener solo el texto
                if palabra_filtro.lower() in nombre_producto.lower():       ## comparamos si la palabra que buscamos esta en el nombre del producto
                    productos_totales.append(nombre_producto)       ## si esta la añadimos a la lista de productos totales
            try:
                boton_siguiente = driver.find_element_by_xpath("//a[span[@class='pagination__next icon-right-arrow-thin']]")
                driver.execute_script("arguments[0].click();", boton_siguiente)
                time.sleep(3)  # Esperar que cargue la siguiente página
            except:
                print("No se pudo encontrar el botón 'Siguiente'.")
                break
        driver.quit() ## cerramos el navegador
    except:
        print(f"error")


def analisis_supermercados(urls_alcampo, urls_carrefour, palabra_filtro):
    productos_totales = []
    
    # Analizar Alcampo
    for url in urls_alcampo:
        print(f"\nAnalizando URL de Alcampo: {url}\n")
        parse_html(url, palabra_filtro, productos_totales)

    # Analizar Carrefour
    for url in urls_carrefour:
        print(f"\nAnalizando URL de Carrefour: {url}\n")
        hlml_carrefour(url, palabra_filtro, productos_totales)

    return productos_totales
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
    "https://www.carrefour.es/supermercado/congelados/cat21449123/c"
    ]
# Pedir la palabra de búsqueda
palabra = input("Seleccione el alimento que desea buscar: ")

# Ejecutar el análisis
productos_filtrados = analisis_supermercados(urls_a_analizar_alcampo, urls_a_analizar_carrefour, palabra)

# Mostrar los productos encontrados
print("\nProductos encontrados:")
for producto in productos_filtrados:
    print(producto)

