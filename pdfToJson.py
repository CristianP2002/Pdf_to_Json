import PyPDF2  # Librería para trabajar con archivos PDF
import json   # Librería para trabajar con datos en formato JSON
import re     # Librería para trabajar con expresiones regulares

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return pdf_reader, pdf_file

# Función para analizar el texto de una página
def parse_page(page_text):
    data = {
        'orden_compra': '',
        'nit': '',
        'comprador' : '',
        'fax' : ''
    }

    # patron para encontrar el orden de compra
    order_pattern = r'Orden\s*de\s*Compra\s*:\s*([\d\s]{10,})'

    # Patrón para encontrar el NIT
    nit_pattern = r'N.I.T\s*:\s*(\d{5,})'
    
    # Patrón para encontrar el comprador, que puede contener espacios
    comprador_pattern = r'Comprador\s*:\s*(.*?)(?=\s*Fax\s*:|$)'
    
    # Patrón para encontrar el fax, que puede contener espacios
    fax_pattern = r'Fax\s*:\s*(.+)'
    
    # Buscar el patrón de orden de compra
    order_match = re.search(order_pattern, page_text, re.IGNORECASE)
    if order_match:
        raw_order_number = order_match.group(1)
        clean_order_number = re.sub(r'\s+', '', raw_order_number)
        if len(clean_order_number) >= 10:
            data['orden_compra'] = clean_order_number
        else:
            print("El numero de orden de compra no se encuentra.")
    else:
        print("No se encontró una orden de compra en la página.")
    

    # Buscar el patrón del NIT
    nit_match = re.search(nit_pattern, page_text, re.IGNORECASE)
    if nit_match:
        data['nit'] = nit_match.group(1)
    else:
        print("No se encontró un NIT válido en la página.")
        
    # Buscar el patrón del comprador
    comprador_match = re.search(comprador_pattern, page_text, re.IGNORECASE)
    if comprador_match:
        data['comprador'] = comprador_match.group(1).strip()
    else:
        print("No se encontró un Comprador válido en la página.")
    
    # Buscar el patrón del fax
    fax_match = re.search(fax_pattern, page_text, re.IGNORECASE)
    if fax_match:
        data['fax'] = fax_match.group(1).strip()
    else:
        print("No se encontró un Fax válido en la página.")
    return data

# Función para convertir la información de cada página en formato JSON
def convert_pages_to_json(pages_data):
    return json.dumps(pages_data, indent=4)

pdf_path = 'ordenCompra.pdf'  # Ruta al archivo PDF
pdf_reader, pdf_file = extract_text_from_pdf(pdf_path)

pages_data = []
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    page_text = page.extract_text()
    if page_text:
        page_data = parse_page(page_text)
        pages_data.append(page_data)
    else:
        print(f"No se pudo extraer texto de la página {page_num + 1}")

pdf_file.close()  # Cerrar el archivo después de leer todas las páginas

json_data = convert_pages_to_json(pages_data)

# Escribir el JSON resultante en un archivo
with open('ordenCompra.json', 'w') as json_file:
    json_file.write(json_data)

print("El contenido del PDF se ha guardado en ordenCompra.json")
