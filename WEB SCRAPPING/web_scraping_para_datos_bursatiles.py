import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
data = requests.get(url).text
soup = BeautifulSoup(data, 'html.parser')

rows_list = []

for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    
    # Solo procesa si tiene 7 columnas
    if len(col) == 7:
        rows_list.append({
            "Date": col[0].text,
            "Open": col[1].text,
            "High": col[2].text,
            "Low": col[3].text,
            "Close": col[4].text,
            "Adj Close": col[5].text,
            "Volume": col[6].text
        })

netflix_data = pd.DataFrame(rows_list)
print(netflix_data)