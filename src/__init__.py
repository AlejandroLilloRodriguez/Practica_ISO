import requests
from bs4 import BeautifulSoup
from plyer import  notification
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.compraonline.alcampo.es/categories?source=navigation"

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

def analisis_url(urls, palabra_filtro):
    productos_totales = []  # Lista para guardar todos los productos
    for url in urls:
        print(f"\nAnalizando URL: {url}\n")
        parse_html(url,palabra_filtro, productos_totales)

    return productos_totales

urls_a_analizar= [
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

palabra= input("Seleccione el alimento que desea buscar:")

productos_filtrados = analisis_url(urls_a_analizar, palabra)

print("\nProductos encontrados:")
for producto in productos_filtrados:
    print(producto)




