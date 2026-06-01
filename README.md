# Proyecto BI sobre finanzas | Analisis de datos
Análisis de datos BI para la deteccion de fraudes a partir de transacciones, bancos, categorias y score de riesgo. Ademas vamos a obtener KPIS como la tasa de fraude por transaccion
filtrando por categorias y bancos a lo largo del año asi como el monto respectivo, entre otros resultados interesantes. Utilizaremos el lenguaje de programación Python implementado el proceso ETL
con un archivo Excel y armar nuestro dashboard con Tableau. 

## 📌 Objetivo del proyecto

Familizarse con el lenguaje de negocios inteligentes, analisis de datos y obtener indicadores clave de desempeño para detectar posibles fraudes por categoria y banco,
ademas de implementar el proceso ETL para nuestro archivo Excel. 

## 🛠️ Tecnologías utilizadas

<p align="left">
  <img src="https://skillicons.dev/icons?i=python,power bi, excel" />
</p>

- Python
- Power BI
- Excel 
- Pandas  

---

## 🧱 Arquitectura del proyecto

<p align="center">
  <img src="grosery.png" width="900"/>
</p>

---

## 🎥 Videos del proyecto

<table>
<tr>

<td align="center">

## 🎥 Explicación en Español

<a href="https://www.youtube.com/watch?v=wUgCyCNnwUU&t">
  <img src="https://img.youtube.com/vi/wUgCyCNnwUU&t/maxresdefault.jpg" width="700"/>
</a>

### 🇺🇸 English Version

<a href="LINK_VIDEO_ENGLISH">
  <img src="https://img.youtube.com/vi/jINcV2zDAk0/maxresdefault.jpg" width="400"/>
</a>

</td>

</tr>
</table>

---

## 📊 Dashboard y visualizaciones

### Dashboard en Power BI

<p align="center">
  <img src="dashboard/actividadcomun.jpg" width="900"/>
</p>

<p align="center">
  <img src="dashboard/foliosprofe.jpg" width="900"/>
</p>

<p align="center">
  <img src="dashboard/usuariosconstantes.jpg" width="900"/>
</p>

---

## ⚙️ Flujo de trabajo del pipeline

1. Archivo Excel que contiene pasarela de bancos, tienda online y monitoreo de riesgo. 
2. Limpieza, validación y transformación de datos utilizando Python con la libreria Pandas.
3. El proceso ETL nos genera un archivo CSV limpio el cual se analizara con Power BI.
4. Implementacion del modelo estrella para poder tener un flujo de trabajo mas ordenado y poder crear calculos eficientemente.
5. Calcular indicadores de desempeño para la posible detaccion de fraudes, categorizando por categoria y banco emisor a lo largo del año.  
6. Visualización y análisis de los datos con Power BI.
---

## 📈 Resultados obtenidos

- Logramos detectar posibles fraudes al filtrar por clientes nuestros resultados en funcion de sus transacciones. 
- En particular para el banco Banamex en la categoria de Belleza se observa una tasa y monto de fraude muy baja. 
- Se obtuvieron con éxito como cambian los indicadores clave de desempeño a lo largo del año, así pudiendo identificar meses donde se presentan mayores posibles fraudes.  

---

## 🧠 Qué aprendí

- Arquitectura basica para analizar datos. 
- Procesos ETL utilizando Python.
- Manejo de Power BI para organizar la información. 
- Diseño de dashboards para la toma de decisiones y propuestas de estrategias. 
- Identificar patrones que nos ayudan a detectar posibles fraudes.
- Familiarizarme con el lenguaje de finanzas y negocios inteligentes. 
---

## 🚀 Futuras mejoras

- Simular eventos con Apache Kafka para detectar fraudes y hacer un analisis de datos en tiempo semi real. 
- Crear modelos predictivos sobre comportamiento de estos indicadores claves de desempeño utilizando modelos de inteligencia artificial.  
