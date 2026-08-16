# Web Scraping para Extracción de Datos de Acciones

Este proyecto contiene un Jupyter Notebook que demuestra cómo realizar web scraping para extraer datos históricos de precios de acciones (específicamente Amazon) de una página web HTML.

## 📋 Descripción

El notebook `uso_webscraping_to_extract_stock_data.ipynb` muestra un proceso completo de:
1. **Descarga de datos HTML** desde una URL remota
2. **Parsing y extracción** de datos usando BeautifulSoup
3. **Estructuración de datos** en un DataFrame de Pandas
4. **Visualización** de los datos extraídos

## 🛠️ Requisitos

Las siguientes librerías necesarias se instalan automáticamente al ejecutar el notebook:

- **pandas** (3.0.3+) - Manipulación y análisis de datos
- **numpy** (2.3.3+) - Computación numérica
- **requests** (2.34.2+) - Descarga de contenido web
- **beautifulsoup4** (4.15.0+) - Parsing de HTML
- **html5lib** (1.1+) - Parser HTML5

## 📊 Estructura de Datos

El notebook extrae información histórica de acciones con las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| **Date** | Fecha del registro (ej: Jan 01, 2021) |
| **Open** | Precio de apertura |
| **High** | Precio máximo del día |
| **Low** | Precio mínimo del día |
| **Close** | Precio de cierre |
| **Adj Close** | Precio de cierre ajustado |
| **Volume** | Volumen de transacciones |

## 🚀 Uso

1. Abre el notebook en Jupyter:
   ```bash
   jupyter notebook uso_webscraping_to_extract_stock_data.ipynb
   ```

2. Ejecuta todas las celdas en orden. El notebook automáticamente:
   - Instalará las dependencias necesarias
   - Descargará los datos de la URL remota
   - Realizará el web scraping
   - Mostrará los primeros registros en una tabla

## 📝 Ejemplo de Salida

```
           Date      Open      High       Low     Close       Volume Adj Close
0  Jan 01, 2021  3,270.00  3,363.89  3,086.00  3,206.20   71,528,900  3,206.20
1  Dec 01, 2020  3,188.50  3,350.65  3,072.82  3,256.93   77,556,200  3,256.93
2  Nov 01, 2020  3,061.74  3,366.80  2,950.12  3,168.04   90,810,500  3,168.04
3  Oct 01, 2020  3,208.00  3,496.24  3,019.00  3,036.15  116,226,100  3,036.15
4  Sep 01, 2020  3,489.58  3,552.25  2,871.00  3,148.73  115,899,300  3,148.73
```

## 💡 Conceptos Clave

### Web Scraping
Técnica de extracción de datos de sitios web mediante:
- Solicitudes HTTP con `requests`
- Parsing de HTML con `BeautifulSoup`
- Extracción selectiva de elementos DOM

### Estructura HTML
El notebook busca:
- Elementos `<tbody>` que contienen las tablas
- Filas `<tr>` con los registros
- Celdas `<td>` con los valores específicos

## 🔗 Fuentes de Datos

- **URL de datos**: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html

## ⚠️ Notas Importantes

- El notebook ignora advertencias de `FutureWarning` para una salida más limpia
- Los datos se combinan usando `pd.concat()` para compatibilidad con versiones recientes de Pandas
- Asegúrate de tener conexión a internet para descargar los datos

## 📚 Referencias

- [Pandas Documentation](https://pandas.pydata.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)

## ✅ Estado

Este notebook es funcional y ha sido probado exitosamente. Está diseñado como material educativo para aprender web scraping con Python.

---

**Autor**: JhonCH11  
**Última actualización**: 2026-08-16
