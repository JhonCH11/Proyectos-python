# Code for ETL operations on Banks data

# Importing the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime


def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("code_log.txt", "a") as log_file:
        log_file.write(timestamp + " : " + message + "\n")


def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''

    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, "html.parser")

    tables = data.find_all("table")

    # Tabla correspondiente a "By market capitalization"
    table = tables[1]

    rows = table.find_all("tr")

    data_list = []

    for row in rows[1:]:
        cols = row.find_all("td")

        if len(cols) >= 3:

            name = cols[1].get_text(strip=True)
            market_cap = cols[2].get_text(strip=True)

            data_list.append([name, market_cap])

    df = pd.DataFrame(data_list, columns=table_attribs)

    # Eliminar el último carácter (\n)
    df["MC_USD_Billion"] = df["MC_USD_Billion"].str[:-1]

    # Convertir a float
    df["MC_USD_Billion"] = df["MC_USD_Billion"].astype(float)

    # Seleccionar los 10 bancos
    df = df.head(10)

    return df


def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''

    exchange_rate_df = pd.read_csv(csv_path)

    exchange_rate = exchange_rate_df.set_index(
        exchange_rate_df.columns[0]
    ).to_dict()[exchange_rate_df.columns[1]]

    # GBP
    gbp_rate = float(exchange_rate["GBP"])

    df["MC_GBP_Billion"] = [
        np.round(x * gbp_rate, 2)
        for x in df["MC_USD_Billion"]
    ]

    # EUR
    eur_rate = float(exchange_rate["EUR"])

    df["MC_EUR_Billion"] = [
        np.round(x * eur_rate, 2)
        for x in df["MC_USD_Billion"]
    ]

    # INR
    inr_rate = float(exchange_rate["INR"])

    df["MC_INR_Billion"] = [
        np.round(x * inr_rate, 2)
        for x in df["MC_USD_Billion"]
    ]

    return df


def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    df.to_csv(output_path, index=False)


def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''

    df.to_sql(table_name, sql_connection, if_exists="replace", index=False)


def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''

    print(query_statement)

    cursor = sql_connection.cursor()
    cursor.execute(query_statement)

    rows = cursor.fetchall()

    for row in rows:
        print(row)


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

# Known values
url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"

table_attribs = ["Name", "MC_USD_Billion"]

csv_path = "exchange_rate.csv"

output_path = "./Largest_banks_data.csv"

database_name = "Banks.db"

table_name = "Largest_banks"


# Tarea 1
log_progress("Preliminares completos. Iniciando proceso ETL")


# Tarea 2
df = extract(url, table_attribs)

log_progress("Extracción de datos completa. Iniciando proceso de Transformación")


# Tarea 3
df = transform(df, csv_path)

log_progress("Transformación de datos completa. Iniciando proceso de Carga")


# Tarea 4
load_to_csv(df, output_path)

log_progress("Datos guardados en archivo CSV")


# Tarea 5
sql_connection = sqlite3.connect(database_name)

log_progress("Conexión SQL iniciada")


load_to_db(df, sql_connection, table_name)

log_progress(
    "Datos cargados en la base de datos como una tabla, ejecutando consultas"
)


# Tarea 6
query1 = "SELECT * FROM Largest_banks"
run_query(query1, sql_connection)

query2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query2, sql_connection)

query3 = "SELECT Name FROM Largest_banks LIMIT 5"
run_query(query3, sql_connection)

log_progress("Proceso completo")


# Tarea 7
sql_connection.close()

log_progress("Conexión al servidor cerrada")