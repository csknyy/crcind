import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import pdfplumber

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
      #try:
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

        data_dict['Country'] = url_country
        
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
        
        ###ACTIVE INGREDIENTS
        response2 = requests.get(safety_data_sheet_url)
        
        with open("downloaded_pdf.pdf", "wb") as pdf_file:
            pdf_file.write(response2.content)
        
        with pdfplumber.open("downloaded_pdf.pdf") as pdf:
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()
        
        if url_country == 'NZ':
          mixtures_index = pdf_text.split('\n').index('Mixtures')
          mixture = pdf_text.split('\n')[mixtures_index + 2 : mixtures_index + 5]
        
          def extract_name(input_string):
              parts = input_string.split(' ')
              name = ' '.join(parts[2:])
              return name
        
          names = [extract_name(i).split(',')[0].title() for i in mixture]
          delimiter= '; '
          ingredients = delimiter.join(names)
          data_dict['Active Ingredients'] = ingredients
        
        elif url_country == 'AU':
          mixtures_index = pdf_text.split('\n').index('3.1 Substances / Mixtures')
          mixtures = [i for i in pdf_text.split('\n')[mixtures_index + 2 : mixtures_index + 6] if '-' in i]
          ingredients = ' '.join([' '.join(i.replace(' to ','').split(' ')[:-3]) for i in mixtures])
          data_dict['Active Ingredients'] = ingredients
        
        ###HAZARD CODE
        if url_country == 'NZ':
          hazard_index = next((index for index, string in enumerate(pdf_text.split('\n')) if '14.3.Transport hazard' in string), None)
          hazard_code = pdf_text.split('\n')[hazard_index].split(' ')[-1]
          data_dict['Hazard Code'] = hazard_code
        
        elif url_country == 'AU':
          hazard_index = pdf_text.split('\n').index('LAND TRANSPORT (ADG) SEA TRANSPORT (IMDG / IMO) AIR TRANSPORT (IATA / ICAO)')
          hazard_code = pdf_text.split('\n')[hazard_index + 4].split(' ')[2]
          data_dict['Hazard Code'] = hazard_code
        
        ###SPECIFICATIONS
        specifications = soup.find('table', class_='data table additional-attributes')
        rows = specifications.find_all('tr')
        for row in rows:
          cells = row.find_all(['th', 'td'])
          if len(cells) == 2:
            label = cells[0].find('span').get_text(strip=True)
            value = cells[1].find('span').get_text(strip=True)
            data_dict[label] = value
        
        data = pd.DataFrame([data_dict])
        
        if url_country == 'NZ':
          data['Product Code'] = data['Product Code:']
        
          del data['Product Code:']
        
          move_to_end = ['Unit Size', 'Unit Package Description', 'Safety Data Sheet', 'Active Ingredients', 'Hazard Code']
        
          data = data[[col for col in data.columns if col not in move_to_end] + move_to_end]
        elif url_country == 'AU':
          move_to_end = ['Unit Dimensions', 'Unit Size', 'Safety Data Sheet', 'Active Ingredients', 'Hazard Code']
        
          data = data[[col for col in data.columns if col not in move_to_end] + move_to_end]

      #except:
      #  pass

    st.dataframe(data)
  
  except Exception as e:
    st.error(f"Error: {e}")
else:
    st.info("Please enter some codes to get started.")
