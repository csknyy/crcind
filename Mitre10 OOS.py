import pandas as pd

data_BSS = pd.read_excel('NZ BSS Report - 26.10.23.xlsx', sheet_name = 'Products below safety stock')

data_M10_ranking = pd.read_excel('M10 Bronze CRC Ranking Report - CRC All Departments - wc 2023-10-16.xlsm', engine = 'openpyxl', skiprows = 5, usecols = list(range(4, 115)), sheet_name = 'Ranking')
data_M10_stock = pd.read_excel('M10 Bronze CRC Ranking Report - CRC All Departments - wc 2023-10-16.xlsm', engine = 'openpyxl', skiprows = 2, usecols = list(range(2, 12)), sheet_name = 'Stock')


data = pd.merge(data_BSS['Legacy'], data_M10_ranking[['Supplier Item Code', 'M10 Code','Item', 'Department', 'Range']], how='left', left_on='Legacy', right_on='Supplier Item Code')

data['SOH Status'] = ''

del data['Supplier Item Code']

data['Next Availabilty Date (NAVD)'] = data_BSS['ETA to Mondiale']

data['Date item went Out of Stock'] = ''
data['Days Out Of Stock'] = ''
data['Mitre 10 Promo'] = ''
data['Supplier Comments'] = ''

data = pd.merge(data, data_M10_ranking[['Supplier Item Code','$Value MAT','Units MAT','SOH LW']], how='left', left_on='Legacy', right_on='Supplier Item Code')

del data['Supplier Item Code']

data = pd.merge(data, data_M10_stock[['Supplier Item Code','WOC ']], how='left', left_on='Legacy', right_on='Supplier Item Code')

del data['Supplier Item Code']

data[' '] = ''

data['Physical inventory'] = data_BSS['Physical inventory']

for i in ['M10 Code', '$Value MAT', 'Units MAT', 'SOH LW', 'WOC ']:
  data[i] = data[i].fillna(0).astype(int)

data = data[(data['Physical inventory']==0) & (data['M10 Code'] != 0)]

del data['Physical inventory']

data
