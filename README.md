# Alumno: David Troitiño Ruiz  --- EDA PROJECT --- Evolve Academy

# Análisis Exploratorio de Datos (EDA) - Turismo Mundial

Este proyecto de EDA se centra en la extracción, limpieza y visualización de datos turísticos a nivel mundial. El flujo de trabajo se divide en tres etapas principales:

1. **Extracción de datos**  
2. **Limpieza de datos**  
3. **Visualización**

---
## 0. Diagrama de proceso

![Diagrama del proyecto EDA](../data/images/EDA_diagram.png)


## 1. Extracción de datos

Para la obtención de los datos se han utilizado dos fuentes principales:

1. **World Bank Group**  
   [https://data360.worldbank.org/en/indicator/WB_WDI_SP_POP_TOTL](https://data360.worldbank.org/en/indicator/WB_WDI_SP_POP_TOTL)  

   - Se extrajo un archivo CSV con datos de población mundial por país y año.

2. **UN Tourism**  
   [https://www.untourism.int/es/onu-turismo-dashboard-datos-turisticos/indicadores-clave-turismo](https://www.untourism.int/es/onu-turismo-dashboard-datos-turisticos/indicadores-clave-turismo)  

   - De este dashboard se extrajeron imágenes PNG con información mensual de turistas en los principales países.  
   - La extracción de datos de estas imágenes se realizó mediante OCR, utilizando la librería `pytesseract`. Esto se debió a que las bases de datos disponibles no tenían suficiente granularidad (solo anual).  
   - El notebook `0_data_extraction.ipynb` detalla el proceso de extracción.  
   - La estructura de trabajo se resume en el siguiente diagrama:

   ![Diagrama del proyecto](../data/images/EDA_diagram.png)

   - Las capturas de imágenes se almacenan en `data/Tourism_jpgs`.  
   - Una vez ejecutadas las funciones del notebook, se generan archivos CSV que se guardan en las carpetas correspondientes.  
   - Posteriormente, en `1_data_cleaning.ipynb` se hace un merge de todos los CSVs para obtener un único dataset con los datos turísticos de cada país.

---

## 2. Limpieza de datos

El dataset requiere un proceso exhaustivo de limpieza, normalización y enriquecimiento. Los pasos aplicados son los siguientes:

1. **Unificación de datasets originales**  
   - Se recorren recursivamente las carpetas de `data/Tourism_jpgs` y se leen los CSV individuales.  
   - Se transforma cada CSV de formato ancho a formato largo (`Year, Month, Country, N_visitors`).  
   - Se concatenan todos los archivos en un único DataFrame `df_final`, guardado posteriormente como `tourism.csv`.

2. **Carga y tipado de columnas**  
   - `Year` y `Month` convertidos a enteros.  
   - `Country` convertido a string.  
   - `N_visitors` se limpia de errores del OCR (`—` en lugar de `-`), convirtiéndose a numérico y finalmente a entero.

3. **Corrección de valores negativos**  
   - Se detectan valores negativos en `N_visitors` por errores del OCR.  
   - Se corrige manualmente el valor inconsistente de Australia (julio 2019).

4. **Análisis y desglose de valores faltantes**  
   - Revisión general de NaNs con `check_nans()`.  
   - Desglose por país y año con `desglose_nans()`.  
   - Se identifican tres causas: ausencia total de datos, datos trimestrales y errores del OCR.

5. **Eliminación de NaNs cuando no existe información**  
   - Se eliminan los valores faltantes en países sin datos para determinados años:  
     `Uzbekistan, United Arab Emirates, Colombia, Vietnam, Morocco, Bulgaria`.

6. **Interpolación lineal en países con datos trimestrales**  
   - Para `Hungary, Poland, Albania`, se aplica interpolación lineal con `interpolar_nans()`.  
   - Se eliminan los NaNs iniciales restantes con `drop_nans()`.

7. **Revisión y eliminación de NaNs finales**  
   - Se revisan los 39 NaNs restantes y se eliminan, asegurando un dataset consistente.

8. **Limpieza de filas erróneas y duplicados**  
   - Se eliminan filas con `Country == "Unnamed: 0"`.  
   - Se corrigen duplicados en Hungría y Polonia.

9. **Reinterpolación y refinado final**  
   - Hungría se reinterpola tras correcciones manuales.  
   - Se eliminan filas finales de Polonia sin datos en 2024.  
   - Se ordena el dataset por `Country, Year, Month`.

10. **Enriquecimiento con datos de población**  
    - Merge con `population_data.csv` para añadir: `Population` y `Ref_country`.  
    - Se corrigen discrepancias en nombres de países (`Turkey → Turkiye`) asegurando consistencia.

11. **Exportación del dataset limpio**  
    - El dataset final se guarda como `data/tourism_clean.csv`.  
    - Este dataset es el utilizado en la fase de visualización y análisis posterior.

---

## 3. Visualización de datos

Para la visualización de los datos se han utilizado librerías como **Matplotlib** y **Seaborn**, permitiendo generar gráficos claros e intuitivos que facilitan el análisis de tendencias turísticas.

A partir de estos gráficos se han obtenido una serie de conclusiones relevantes:

- **Impacto del COVID en el turismo global (2020-2022):**  
  Los gráficos muestran claramente la caída drástica de visitantes a nivel mundial durante los años 2020, 2021 y 2022 debido a las restricciones de movilidad y cierres de fronteras. Esta información permite cuantificar el efecto de la pandemia y comparar la recuperación de los distintos países en años posteriores.

- **Países con mayor turismo en los últimos años:**  
  Mediante la agregación y comparación de los datos anuales, se identifican los destinos más visitados. Esto permite no solo conocer qué países reciben más turistas, sino también detectar cambios en tendencias a lo largo del tiempo, como el crecimiento de ciertos destinos emergentes frente a los tradicionales.

- **Meses con menor y mayor número de turistas por país:**  
  El análisis mensual revela patrones estacionales en la llegada de turistas. Esta información permite a cualquier usuario:  
  - Identificar tendencias estacionales y picos de turismo en cada país.  
  - Elegir los mejores meses para viajar evitando las épocas de mayor afluencia.  
  - Planificar viajes más eficientes y confortables, evitando grandes aglomeraciones.  
  - En un futuro, esta información podría integrarse en un algoritmo que sugiera automáticamente los destinos menos turísticos según las fechas de vacaciones de un usuario, optimizando la experiencia de viaje y reduciendo la congestión en los destinos más populares.

En conjunto, estas visualizaciones no solo facilitan la comprensión de los datos, sino que también aportan valor práctico tanto para análisis estratégicos como para la planificación turística personal.


