"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import glob
import os

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
    df_clean = df.copy()

    df_clean['sexo'] = df_clean['sexo'].str.lower().astype('category')
    
    fecha_col = "fecha_de_beneficio"
    df_clean[fecha_col] = pd.to_datetime(
        df_clean[fecha_col], format="%d/%m/%Y", errors="coerce"
    ).combine_first(
        pd.to_datetime(df_clean[fecha_col], format="%Y/%m/%d", errors="coerce")
    )

    df_clean['monto_del_credito'] = (
        df_clean['monto_del_credito']
        .str.strip()
        .str.replace(r'[$,]', '', regex=True)
        .str.replace('.00', '', regex=False)
        .astype(int)
    )

    df_clean['barrio'] = df_clean['barrio'].str.lower().str.replace(r'[_-]', ' ', regex=True)
    
    cols = ['idea_negocio', 'línea_credito', 'tipo_de_emprendimiento']
    for col in cols:
        df_clean[col] = (
            df_clean[col]
            .str.lower()
            .str.replace(r'[_-]', ' ', regex=True)
            .str.strip()
        )

    df_clean = df_clean.drop_duplicates().dropna()

    output_dir = 'files/output/'
    os.makedirs(output_dir, exist_ok=True)
    df_clean.to_csv(os.path.join(output_dir, 'solicitudes_de_credito.csv'), sep=';', index=True)
    
    return df_clean


if __name__ == "__main__":
    pregunta_01()