import json
import nbformat as nbf

def jupyter_to_zeppelin(jupyter_file, zeppelin_file):
    with open(jupyter_file, 'r', encoding='utf-8') as jf:
        jupyter_nb = nbf.read(jf, as_version=4)
    
    zeppelin_nb = {
        'name': 'Notebook Name',  # Puedes cambiar el nombre del notebook aquí
        'paragraphs': [],
        'version': '0.9.0'  # La versión de Zeppelin, ajusta si es necesario
    }
    
    for cell in jupyter_nb['cells']:
        paragraph = {
            'text': ''.join(cell['source']),
            'config': {
                'editorMode': 'ace/mode/markdown' if cell['cell_type'] == 'markdown' else 'ace/mode/python'
            },
            'result': {}
        }
        zeppelin_nb['paragraphs'].append(paragraph)

    with open(zeppelin_file, 'w', encoding='utf-8') as zf:
        json.dump(zeppelin_nb, zf, ensure_ascii=False, indent=2)

# Reemplaza 'GRAFO_FINAL.ipynb' 
#jupyter_file = 'preprocesing_FOS.ipynb'
jupyter_file = 'training-torch-nn.ipynb'
# Reemplaza 'GRAFO_FINAL.json'
zeppelin_file = 'training-torch-nn.json'

jupyter_to_zeppelin(jupyter_file, zeppelin_file)
