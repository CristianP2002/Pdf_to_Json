import PyPDF2  # Librería para trabajar con archivos PDF
import json   # Librería para trabajar con datos en formato JSON
import re     # Librería para trabajar con expresiones regulares

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    pdf_file = open(pdf_path, 'rb') 
    pdf_reader = PyPDF2.PdfReader(pdf_file) 
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num] 
        text += page.extract_text() + "\n"
    pdf_file.close() 
    return text 

# Función para analizar el texto en secciones específicas
def parse_sections(text):
    sections = { 
        'inicio': '',
        'nudo': '',
        'desenlace': ''
    }

    patterns = {
        'inicio': r'Inicio:\s*(.*)',
        'nudo': r'Nudo:\s*(.*)',
        'desenlace': r'Desenlace:\s*(.*)'
    }

    current_section = None  # Variable para rastrear la sección actual
    lines = text.split('\n') 

    for line in lines:
        for section, pattern in patterns.items():
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                current_section = section
                sections[section] += match.group(1) + '\n'
                break
        else:
            if current_section:
                sections[current_section] += line + '\n'

    return sections

# Función para convertir las secciones en formato JSON
def convert_sections_to_json(sections):
    return json.dumps(sections, indent=4)

pdf_path = 'doc1.pdf'  # Ruta al archivo PDF
extracted_text = extract_text_from_pdf(pdf_path)
sections = parse_sections(extracted_text)
json_data = convert_sections_to_json(sections)

# Escribir el JSON resultante en un archivo
with open('doc1.json', 'w') as json_file:
    json_file.write(json_data)

print("El contenido del PDF se ha guardado en doc1.json")
