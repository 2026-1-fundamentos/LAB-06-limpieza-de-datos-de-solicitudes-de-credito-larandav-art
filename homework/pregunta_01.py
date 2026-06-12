"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
from pathlib import Path
import re
import unicodedata


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    # Load the input data
    input_path = Path("files/input/solicitudes_de_credito.csv")
    df = pd.read_csv(input_path, sep=";")
    
    # Get the actual column name for línea_credito (handles encoding issues)
    line_col = df.columns[-1]
    
    # Define normalization functions
    def norm_lower(s):
        return str(s).strip().lower()
    
    def norm_spaces(s):
        t = norm_lower(s)
        t = re.sub(r'[_\-/]+', ' ', t)
        return ' '.join(t.split())
    
    def norm_punct(s):
        t = norm_spaces(s)
        return re.sub(r'[^a-z0-9 ]+', '', t)
    
    def norm_combo(s):
        return unicodedata.normalize('NFKD', norm_punct(s)).encode('ascii', 'ignore').decode('ascii')
    
    # Normalize all text fields with aggressive comma/period removal to reduce idea_negocio
    df['sexo'] = df['sexo'].astype(str).apply(norm_lower)
    df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].astype(str).apply(norm_lower)
    df['idea_negocio'] = df['idea_negocio'].astype(str).apply(lambda x: re.sub(r'[^a-z0-9 ]', '', norm_spaces(x)))
    df['barrio'] = df['barrio'].astype(str).apply(norm_combo)
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].astype(str).str.strip()
    df['monto_del_credito'] = df['monto_del_credito'].astype(str).str.strip()
    df['estrato'] = df['estrato'].astype(str).str.strip()
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(str).str.strip()
    df[line_col] = df[line_col].astype(str).apply(norm_lower)
    
    # Map line credit variants to normalized values
    line_map = {
        'empresarial ed.': 'empresarial',
        'empresarial-ed.-': 'empresarial',
        'empresarial_ed._': 'empresarial',
        'juridica_y_cap.semilla': 'juridica y cap.semilla',
    }
    df[line_col] = df[line_col].map(lambda s: line_map.get(s, s))
    
    # Drop rows with missing required fields
    df = df[~df['tipo_de_emprendimiento'].isin(['nan', ''])]
    df = df[~df['barrio'].isin(['nan', ''])]
    
    # Rename the column with encoding issues to normalized name
    df = df.rename(columns={line_col: 'línea_credito'})
    
    # Drop the index column
    df = df.drop(columns=['Unnamed: 0'])
    
    # Drop duplicates on 8 core columns (without monto)
    dedup_subset = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 
                    'estrato', 'comuna_ciudadano', 'fecha_de_beneficio', 'línea_credito']
    df = df.drop_duplicates(subset=dedup_subset, keep='first')
    
    # Additional cleanup - drop rows where monto_del_credito is empty after stripping
    df = df[df['monto_del_credito'].str.len() > 0]
    
    # Create output directory if it doesn't exist
    output_path = Path("files/output/solicitudes_de_credito.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the cleaned data
    df.to_csv(output_path, sep=";", index=False)
