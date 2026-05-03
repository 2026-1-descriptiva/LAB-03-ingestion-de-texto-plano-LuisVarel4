"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import pandas as pd
    import re

    with open('files/input/clusters_report.txt', 'r') as f:
        lines = f.readlines()

    data = []
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = []

    for line in lines[4:]:  # Skip header lines
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit():
            # Save previous cluster if exists
            if current_cluster is not None:
                keywords_str = ' '.join(current_keywords)
                keywords_list = [kw.strip().rstrip('.') for kw in keywords_str.split(',') if kw.strip()]
                keywords_list = [' '.join(kw.split()) for kw in keywords_list]  # normalize spaces
                principales_palabras_clave = ', '.join(keywords_list)
                data.append({
                    'cluster': current_cluster,
                    'cantidad_de_palabras_clave': current_cantidad,
                    'porcentaje_de_palabras_clave': current_porcentaje,
                    'principales_palabras_clave': principales_palabras_clave
                })
            # Parse new cluster line
            parts = line.split()
            current_cluster = int(parts[0])
            current_cantidad = int(parts[1])
            current_porcentaje = float(parts[2].replace(',', '.').replace('%', ''))
            # Keywords start after %
            keyword_start = line.find('%') + 1
            keywords_part = line[keyword_start:].strip()
            current_keywords = [keywords_part]
        else:
            # Continuation of keywords
            current_keywords.append(line)

    # Don't forget the last cluster
    if current_cluster is not None:
        keywords_str = ' '.join(current_keywords)
        keywords_list = [kw.strip().rstrip('.') for kw in keywords_str.split(',') if kw.strip()]
        keywords_list = [' '.join(kw.split()) for kw in keywords_list]  # normalize spaces
        principales_palabras_clave = ', '.join(keywords_list)
        data.append({
            'cluster': current_cluster,
            'cantidad_de_palabras_clave': current_cantidad,
            'porcentaje_de_palabras_clave': current_porcentaje,
            'principales_palabras_clave': principales_palabras_clave
        })

    df = pd.DataFrame(data)
    return df
