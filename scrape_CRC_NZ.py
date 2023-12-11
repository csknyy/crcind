import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Collect web data from CRC", layout="wide")


url_country = st.radio("Which country?", ("NZ", "AU"))

if url_country == 'NZ':
  url_base = 'https://www.crc.co.nz/'
elif url_country == 'AU':
  url_base = 'https://crcindustries.com.au/'
elif url_country == 'US':
  url_base = 'https://crcindustries.com/'

data = pd.DataFrame()

crc_codes = st.text_input('Enter commas between item codes')

if len(crc_codes)>0:
  try:
    for i in crc_codes.split(','):
      url = url_base + 'catalogsearch/result/?q=' + str(i)

      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      try:
        url2 = soup.find('a', class_="product-item-link").get('href')
        response = requests.get(url2)
        soup = BeautifulSoup(response.content, 'html.parser')
      except:
        pass
      
      data_dict = {}
      
      ###ITEM NAME
      item_name = soup.find('div', class_='page-title-wrapper product').find('span', class_='base', itemprop='name').get_text(strip=True)
      data_dict['Item Name'] = item_name
      
      ###PRODUCT CODE
      #product_code = soup.find('div', class_='product attribute product_number').find('div', class_='value', itemprop='product_number').get_text(strip=True)
      data_dict['Product Code'] = ''
      
      ###DESCRIPTION
      description = soup.find('div', class_='product-page-description').find('h3', string='DESCRIPTION').find_next('div', class_='value').get_text(strip=True)
      data_dict['Description'] = description
      
      ###APPLICATIONS
      applications = soup.find('div', class_='product-applications').find('p').get_text(strip=True).replace(':', ': ').replace('.', '. ')
      data_dict['Applications'] = applications
      
      ###FEATURES/BENEFITS
      feats_bens = soup.find('div', class_='product-applications').find('p').get_text(strip=True).replace(':', ': ').replace('.', '. ')
      data_dict['Features/Benefits'] = feats_bens
      
      ###SAFETY DATA SHEET URL
      safety_data_sheet_url = soup.find('div', class_='box-tocart').find('a', class_='dropdown-item').get('href')
      data_dict['Safety Data Sheet'] = safety_data_sheet_url
      
      ###SPECIFICATIONS
      specifications = soup.find('table', class_='data table additional-attributes')
      rows = specifications.find_all('tr')
      for row in rows:
        cells = row.find_all(['th', 'td'])
        if len(cells) == 2:
          label = cells[0].find('span').get_text(strip=True)
          value = cells[1].find('span').get_text(strip=True)
          data_dict[label] = value
      
      data_temp = pd.DataFrame([data_dict])

      data = pd.concat([data, data_temp], ignore_index=True)
      
    if url_country == 'NZ':
      data['Product Code'] = data['Product Code:']
    
      del data['Product Code:']
    
      move_to_end = ['Unit Size', 'Unit Package Description', 'Safety Data Sheet']
    
      data = data[[col for col in data.columns if col not in move_to_end] + move_to_end]
    elif url_country == 'AU':
      move_to_end = ['Unit Dimensions', 'Unit Size', 'Safety Data Sheet']
    
      data = data[[col for col in data.columns if col not in move_to_end] + move_to_end]
        
    
    st.dataframe(data)
  
  except Exception as e:
    st.error(f"Error: {e}")
else:
    st.info("Please enter some codes to get started.")
