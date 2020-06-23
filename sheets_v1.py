#!/usr/bin/env python3
# sheets.py

import sys
if len(sys.argv) != 2:
    raise SystemExit("Usage 2 items:\n1. Script to run\n2. Enter amount of gold invested (in grams)")

gold_invested = sys.argv[1]

# Import packages for sheets & scraping
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import re
from bs4 import BeautifulSoup

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

# Set up credentials and connect to Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)  #You have to get & activate your own creds
client = gspread.authorize(creds)

# Open spreadsheet
#client.create('gold_price')
sheet = client.open('gold_price').sheet1

# Format header row
headerRow = 'A1:C1'
sheet.format(headerRow, {'textFormat': {'bold': True, 'fontSize': 12}})
sheet.update(headerRow, [['Date', 'GS Central Buys', f'{gold_invested}GM']])

# Retrieve values
# row = sheet.row_values(2)
# col = sheet.col_values(3)
# cell = sheet.cell(1,2).value

# Webscrape gold prices
url = 'https://www.goldsilvercentral.com.sg/'
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, features='lxml')

spanTag_gold = soup.find("span", {"style": "font-weight:200"})  # Gold price
spanTag_date = soup.find("span", {"style": "font-weight:200; font-style: italic;"}) # Date price was updated

gold_price = spanTag_gold.text[4:] # Convert price to text
date_updated = spanTag_date.text # Convert date to text

# Function to parse new info from web scraper
def newLine(date, gold_oz, gold_invested):
    date = re.search(r"\d{2}/\d{2}/\d{4}", date).group(0)
    pricebought_gram = float(gold_oz) * 3.52   # Converts from 1oz to 100gm
    gold_worth = float(gold_invested) * (pricebought_gram/100)

    # Update in Sheets
    val = [date, pricebought_gram, gold_worth]
    sheet.insert_row(val, index=2)

newLine(date_updated, gold_price, gold_invested)

# Update values in Sheets
# sheet.insert_row(row, 'test')
# sheet.delete_row(4)
# sheet.update_cell(2,2, "peter")

# numRows = sheet.row_count

# Getting All Values From a Worksheet as a List of Dictionaries
# data = sheet.get_all_records()
# print(data)

# pprint(row)
# pprint(col)
# pprint(cell)
# pprint(numRows)