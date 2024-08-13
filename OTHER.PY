import json   # Librería para trabajar con datos en formato JSON
import re     # Librería para trabajar con expresiones regulares
from pdfminer.high_level import extract_text # Librería para trabajar con PDF miner

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Función para analizar el texto de una página
def parse_page(page_text):
    data = {
        'orden_compra': '',
        'nit': '',
        'ciudad': '',
        'direccion': '',
        'telefono': '',
        'comprador': '',
        'fax_comprador': '',
        'total': '',
    }
    
    # Patrones para encontrar la información
    patterns = {
        'orden_compra': r'Orden\s*de\s*Compra\s*:\s*([\d\s]{10,})',
        'nit': r'N\.I\.T\s*:\s*(\d{9,})',
        'ciudad': r'Ciudad\s*:\s*([^\n\r]+)',
        'direccion': r'Dirección\s*:\s*([^\n\r]+)',
        'telefono': r'Teléfono\s*:\s*([^\n\r]+)',
        'comprador': r'Comprador\s*:\s*([^\n\r]+)',
        'fax_comprador': r'Fax\s*:\s*([^\n\r]+)',
        'total': r'Total\s*Impuestos\s*([^\n\r]+)'
    }

    # Buscar cada patrón en el texto de la página
    for key, pattern in patterns.items():
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            data[key] = match.group(1).strip()
        else:
            print(f"No se encontró un {key} válido en la página.")

    # Limpiar el número de orden de compra
    if data['orden_compra']:
        raw_order_number = data['orden_compra']
        clean_order_number = re.sub(r'\s+', '', raw_order_number)
        if len(clean_order_number) >= 10:
            data['orden_compra'] = clean_order_number
        else:
            print("El número de orden de compra no es válido.")
    
    return data

# Función para convertir la información de cada página en formato JSON
def convert_pages_to_json(pages_data):
    return json.dumps(pages_data, indent=4)

# Cambia esta ruta a la ubicación de tu archivo PDF
pdf_path = 'ordenCompra.pdf'
text = extract_text_from_pdf(pdf_path)

pages_data = []

# Dividir el texto en páginas (pdfminer extrae todo el texto junto)
pages = text.split('\f')
for page_num, page_text in enumerate(pages):
    if page_text.strip():
        page_data = parse_page(page_text)
        pages_data.append(page_data)
    else:
        print(f"No se pudo extraer texto de la página {page_num + 1}")

json_data = convert_pages_to_json(pages_data)

# Escribir el JSON resultante en un archivo
with open('ordenCompra.json', 'w') as json_file:
    json_file.write(json_data)

print("El contenido del PDF se ha guardado en ordenCompra.json")
