import csv
import json
from xml.etree import ElementTree as ET
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

def convert_stocklist(xml_path, exchange_map_path, csv_output_path):
    # Read XML data from file
    xml_data = open(xml_path, 'r').read()
    tree = ET.fromstring(xml_data)

    # Load exchange symbol map from JSON
    with open(exchange_map_path, 'r') as json_ex_map:
        exchange_map = json.load(json_ex_map)

    print("Converting...")

    count = 0
    csv_output = []

    for industry in tree.iter('industry'):
        industry_name = industry.attrib['name']
        for company in industry.findall('company'):
            co_name = company.attrib['name']
            co_symbol = company.attrib['symbol']

            co_ex_country = "United States of America"  # NASDAQ, DOW, NYSE don't have symbols
            co_ex_name = ""

            for ex_country, ex_names in exchange_map.items():
                for ex_name, ex_symbol in ex_names.items():
                    if '.' in co_symbol and ('.' + co_symbol.split('.')[1].upper()) == ex_symbol.upper():
                        co_ex_country = ex_country
                        co_ex_name = ex_name

            csv_entry = (co_symbol.encode('utf-8'), co_name.encode('utf-8'), industry_name.encode('utf-8'),
                         co_ex_country.encode('utf-8'), co_ex_name.encode('utf-8'))
            csv_output.append(csv_entry)
            count += 1

    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('YAHOO TICKER', 'COMPANY NAME', 'INDUSTRY', 'COUNTRY TRADED', 'EXCHANGE'))
        writer.writerows(csv_output)

    print("Finished!", count, "stocks were converted to", csv_output_path)

# Example usage:
convert_stocklist('full_stocklist_xml.xml', 'exchange_symbol_map.json', 'yahoo_stocklist.csv')
