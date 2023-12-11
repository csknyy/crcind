import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Collect web data from CRC", layout="wide")

data = pd.DataFrame()

crc_codes = st.text_input('Enter commas between cods')

#crc_codes = '5022,5023'

for i in crc_codes.split(','):
  url = 'https://www.crc.co.nz/catalogsearch/result/?q=' + str(i)

  response = requests.get(url)

  url2 = response.text.split('<a class="product-item-link"\n                                              href="')[1].split('">')[0]

  response = requests.get(url2)

  html_content = response.content

  soup = BeautifulSoup(html_content, 'html.parser')

  data_dict = {}

  ###ITEM NAME
  item_name = soup.find('h1', class_='page-title').find('span', class_='base', itemprop='name').get_text(strip=True)
  data_dict['Item name'] = item_name

  ###PRODUCT CODE
  product_code = soup.find('div', class_='value', itemprop='product_number').get_text(strip=True)
  data_dict['Product code'] = product_code

  ###DESCRIPTION
  description = soup.find('div', class_='product-page-description').find('h3', string='DESCRIPTION').find_next('div', class_='value', itemprop='description').get_text(strip=True)
  data_dict['Description'] = description

  ###APPLICATIONS
  applications = applications = soup.find('div', class_='product-applications').find('p').get_text(strip=True).replace(':', ': ').replace('.', '. ')
  data_dict['Applications'] = applications

  ###FEATURES/BENEFITS
  feats_bens = soup.find('div', class_='product-feature-benefits').find('p').get_text(strip=True).replace(':', ': ').replace('.', '. ')
  data_dict['Features/Benefits'] = feats_bens

  ###SPECIFICATIONS
  specifications = soup.find('table', class_='data table additional-attributes')
  rows = specifications.find_all('tr')
  for row in rows:
    cells = row.find_all(['th', 'td'])
    if len(cells) == 2:
      label = cells[0].find('span').get_text(strip=True)
      value = cells[1].find('span').get_text(strip=True)
      data_dict[label] = value

  '''print(f'Item name \n{item_name}\n')
  print(f'Product code \n{product_code}\n')
  print(f'Description \n{description}\n')
  print(f'Applications \n{applications}\n')
  print(f'Features/Benefits \n{feats_bens}\n')
  print(f'Specifications \n')
  for label, value in data_dict.items():
          print(f"{label}: {value}")'''

  data_temp = pd.DataFrame([data_dict])

  data = pd.concat([data, data_temp], ignore_index=True)

del data['Product Code:']

move_to_end = ['Unit Size', 'Unit Package Description']

data = data[[col for col in data.columns if col not in move_to_end] + move_to_end]

st.dataframe(data)
