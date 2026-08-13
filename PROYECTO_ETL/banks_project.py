# Code for ETL operations on Country-GDP data

# Importing the required libraries
import requests
import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ['Name', 'MC_USD_Billion']
csv_path = './exchange_rate.csv'
output_csv_path = './Largest_banks_data.csv'
db_name = 'Banks.db'
table_name = 'Largest_banks'
log_file = 'code_log.txt'


def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestamp + ' : ' + message + '\n')


def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')

    df = pd.DataFrame(columns=table_attribs)

    # La tabla requerida es la primera tabla con clase 'wikitable' en la página
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            # El primer <a> suele ser el ícono de bandera; el segundo tiene
            # el atributo 'title' con el nombre limpio del banco.
            links = col[1].find_all('a')
            if len(links) > 1:
                data_dict = {
                    "Name": links[1]['title'],
                    "MC_USD_Billion": float(col[2].contents[0][:-1])
                }
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df, df1], ignore_index=True)

    return df


def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    exchange_rate_df = pd.read_csv(csv_path)
    exchange_rate = exchange_rate_df.set_index('Currency').to_dict()['Rate']

    gbp_rate = float(exchange_rate['GBP'])
    eur_rate = float(exchange_rate['EUR'])
    inr_rate = float(exchange_rate['INR'])

    df['MC_GBP_Billion'] = [np.round(x * gbp_rate, 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * eur_rate, 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * inr_rate, 2) for x in df['MC_USD_Billion']]
    
    return df


def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path, index=False)


def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


''' Aquí se definen las entidades requeridas y se llaman las funciones
relevantes en el orden correcto para completar el proyecto. '''

log_progress('Preliminares completos. Iniciando proceso ETL')

df = extract(url, table_attribs)
log_progress('Extracción de datos completa. Iniciando proceso de Transformación')

df = transform(df, csv_path)
log_progress('Transformación de datos completa. Iniciando proceso de Carga')

load_to_csv(df, output_csv_path)
log_progress('Datos guardados en archivo CSV')

sql_connection = sqlite3.connect(db_name)
log_progress('Conexión SQL iniciada')

load_to_db(df, sql_connection, table_name)
log_progress('Datos cargados en la base de datos como una tabla, ejecutando consultas')

# Consulta 1: contenido de toda la tabla
run_query(f'SELECT * FROM {table_name}', sql_connection)

# Consulta 2: capitalización de mercado promedio en GBP
run_query(f'SELECT AVG(MC_GBP_Billion) FROM {table_name}', sql_connection)

# Consulta 3: nombres de los 5 principales bancos
run_query(f'SELECT Name FROM {table_name} LIMIT 5', sql_connection)

log_progress('Proceso completo')

sql_connection.close()
log_progress('Conexión al servidor cerrada') 