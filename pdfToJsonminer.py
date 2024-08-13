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
    
    # Patrón para encontrar el orden de compra (solo los números)
    order_pattern = r'Orden\s*de\s*Compra\s*:\s*([\d\s]{10,})'

    # Patrón para encontrar el NIT (solo números)
    nit_pattern = r'N\.I\.T\s*:\s*(\d{9,})'
    
    # Ejemplo de patrón para encontrar la ciudad
    ciudad_pattern = r'Ciudad\s*:\s*([^\n\r]+)'
    
    # Ejemplo de patrón para encontrar la direccion
    direccion_pattern = r'Dirección\s*:\s*([^\n\r]+)'
    
    # Ejemplo de patrón para encontrar el teléfono
    telefono_pattern = r'Teléfono\s*:\s*([^\n\r]+)'
    
    # Patrón para encontrar el comprador hasta la palabra "Fax"
    comprador_pattern = r'Comprador\s*:\s*([^\n\r]+)'
    
    # Patrón para encontrar el fax
    fax_comprador_pattern = r'Fax\s*:\s*([^\n\r]+)'
    
    # Patrón para encontrar el fax
    total_pattern = r'Total\s*Impuestos\s*([^\n\r]+)'


    # Buscar el patrón de orden de compra
    order_match = re.search(order_pattern, page_text, re.IGNORECASE)
    if order_match:
        raw_order_number = order_match.group(1)
        clean_order_number = re.sub(r'\s+', '', raw_order_number)
        if len(clean_order_number) >= 10:
            data['orden_compra'] = clean_order_number
        else:
            print("El número de orden de compra no se encuentra.")
    else:
        print("No se encontró una orden de compra en la página.")

    # Buscar el patrón del NIT
    nit_match = re.search(nit_pattern, page_text, re.IGNORECASE)
    if nit_match:
        data['nit'] = nit_match.group(1)
    else:
        print("No se encontró un NIT válido en la página.")
        
    # Buscar el patrón del comprador
    comprador_match = re.search(comprador_pattern, page_text, re.MULTILINE)
    if comprador_match:
        data['comprador'] = comprador_match.group(1).strip()
    else:
        print("No se encontró un Comprador válido en la página.")
    
    # Buscar el patrón del fax
    fax_match = re.search(fax_comprador_pattern, page_text, re.IGNORECASE)
    if fax_match:
        data['fax_comprador'] = fax_match.group(1).strip()
    else:
        print("No se encontró un Fax válido en la página.")
    
    # Buscar el patrón de la ciudad
    ciudad_match = re.search(ciudad_pattern, page_text, re.IGNORECASE)
    if ciudad_match:
        data['ciudad'] = ciudad_match.group(1).strip()
    else:
        print("No se encontró una Ciudad válida en la página.")
    
    # Buscar el patrón del teléfono
    telefono_match = re.search(telefono_pattern, page_text, re.IGNORECASE)
    if telefono_match:
        data['telefono'] = telefono_match.group(1).strip()
    else:
        print("No se encontró un Teléfono válido en la página.")
        
    # Buscar el patrón de la direccion
    direccion_match = re.search(direccion_pattern, page_text, re.IGNORECASE)
    if direccion_match:
        data['direccion'] = direccion_match.group(1).strip()
    else:
        print("No se encontró una direccion válido en la página.")
    
    total_match = re.search(total_pattern, page_text, re.IGNORECASE)
    if total_match:
        data['total'] = total_match.group(1).strip()
    else:
        print("No se encontró una direccion válido en la página.")
    
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
