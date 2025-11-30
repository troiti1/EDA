import pandas as pd
import numpy as np

# Función para hacer un checkeo de nans
def check_nans(df):
    nans_pais = df.groupby('Country')['N_visitors'].apply(lambda x: x.isna().sum())
    # Filtramos solo aquellos con NaNs
    nans_pais = nans_pais[nans_pais > 0]
    # Ordenamos de mayor a menor
    nans_pais = nans_pais.sort_values(ascending=False)
    # Printeamos el total y el resto desglosado
    print(f"Total de NaNs: {nans_pais.sum()}")
    print("Total desglosado:")
    print(nans_pais)

# Función para profundizar en los Nans por mes y país
def desglose_nans(df, lista_paises):
    resultado = {}
    
    for pais in lista_paises:
        # Filtrar solo el país
        df_pais = df[df['Country'] == pais]
        
        # Contar NaNs por año
        nans_año = df_pais.groupby('Year')['N_visitors'].apply(lambda x: x.isna().sum())
        
        # Años con al menos un NaN
        años_nan = nans_año[nans_año > 0].index.tolist()
        
        # Convertir nans_año a diccionario
        nans_por_año = nans_año.to_dict()
        
        # Guardar resultados
        resultado[pais] = {
            'años_nan': años_nan,
            'nans_por_año': nans_por_año
        }
    
    return resultado

# Función para dropear nans a partir de una lista de países
def drop_nans(df, paises_nans):
    """
    Elimina filas completas donde N_visitors es NaN, 
    pero solo para los países incluidos en `countries`.
    """
    # Filas de países NO afectados → se quedan completas
    df_keep = df[~df['Country'].isin(paises_nans)]
    
    # Filas de países afectados → eliminar NaNs en N_visitors
    df_clean = df[df['Country'].isin(paises_nans)].dropna(subset=['N_visitors'])
    
    # Unir resultado final
    df = pd.concat([df_keep, df_clean], ignore_index=True)

    return df

# Función para interpolar nans cada x meses
def interpolar_nans(df, paises_interp):

    df_result = df.copy()
    df_result['N_visitors'] = df_result['N_visitors'].astype(float)  # convertir a float
    for pais in paises_interp:
        mask = df_result['Country'] == pais
        df_pais = df_result.loc[mask].sort_values(['Year', 'Month'])
        df_result.loc[mask, 'N_visitors'] = df_pais['N_visitors'].interpolate(method='linear')
    
    # Convertir a int nuevamente si quieres
    df_result['N_visitors'] = df_result['N_visitors'].round(0).astype('Int64')
    return df_result


# Función para cruzar la tabla de turismo y poblacion de cada país
def add_poblacion(df_visitors, df_population):

    df_vis = df_visitors.copy()
    df_pop = df_population.copy()

    # Normalizar nombres de países
    df_vis['Country_lower'] = df_vis['Country'].str.lower()
    df_pop['Country_lower'] = df_pop['REF_AREA_LABEL'].str.lower()

    # Seleccionar columnas de años
    years = [col for col in df_pop.columns if col.isdigit()]

    # Crear versión "long" de df_population sin melt
    pop_long = pd.DataFrame({
        'Country_lower': np.repeat(df_pop['Country_lower'].values, len(years)),
        'Year': np.tile([int(y) for y in years], len(df_pop)),
        'Population': df_pop[years].values.flatten(),
        'Ref_country': np.repeat(df_pop['REF_AREA'].values, len(years))
    })

    # Merge con df_visitors
    df_merged = df_vis.merge(pop_long, on=['Country_lower', 'Year'], how='left')

    # Convertir Population a entero (Int64 permite NaN)
    df_merged['Population'] = df_merged['Population'].round(0).astype('Int64')

    # Convertir Ref_country a string
    df_merged['Ref_country'] = df_merged['Ref_country'].astype('string')
    # Convertimos tambien country nuevamente en un string
    df_merged['Country'] = df_merged['Country'].astype("string")

    # Borrar columna auxiliar
    df_merged.drop(columns=['Country_lower'], inplace=True)

    return df_merged

