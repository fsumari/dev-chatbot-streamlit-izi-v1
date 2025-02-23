import json
import nbformat as nbf

def zeppelin_to_jupyter(zeppelin_file, jupyter_file):
    # Cambia la codificación a 'utf-8-sig' para manejar el BOM
    with open(zeppelin_file, 'r', encoding='utf-8-sig') as zf:
        zeppelin_data = json.load(zf)
    
    jupyter_nb = nbf.v4.new_notebook()
    cells = []

    for paragraph in zeppelin_data['paragraphs']:
        if 'text' in paragraph:
            source = paragraph['text']
            if paragraph['config'].get('editorMode') == 'ace/mode/markdown':
                cell_type = 'markdown'
            else:
                cell_type = 'code'
            
            cell = nbf.v4.new_markdown_cell(source) if cell_type == 'markdown' else nbf.v4.new_code_cell(source)
            cells.append(cell)

    jupyter_nb['cells'] = cells

    with open(jupyter_file, 'w', encoding='utf-8') as jf:
        nbf.write(jupyter_nb, jf)

# Reemplaza 'INCA_NETWORK_ANALYSIS_IMPORTADORES.json' con el nombre de tu archivo de Zeppelin
#zeppelin_file = 'preprocesing_FS.json'
zeppelin_file = 'training-torch.zpln'  
# Reemplaza 'INCA_NETWORK_ANALYSIS_IMPORTADORES.ipynb' con el nombre del archivo de Jupyter que quieres crear
jupyter_file = 'training-torch-nn.ipynb'

zeppelin_to_jupyter(zeppelin_file, jupyter_file)
