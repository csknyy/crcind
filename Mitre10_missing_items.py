import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mitre 10 missing items", layout="wide")

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
  try:  
    data = pd.read_excel(uploaded_file, sheet_name="RangeGaps", header = 1)

    sales_rep_dict = {"A3 Ashby's Mitre 10":"Bruce Gasson", "B7 Beachlands Mitre 10":"Ronny Hewson", "B7T Beachlands Trade Centre":"Ronny Hewson", "C8 Central Otago Mitre 10":"Bruce Gasson", "C7 Crofton Downs Mitre 10":"Bruce Gasson",
                      "C28 Cromwell Mitre 10":"Bruce Gasson", "W7 Dannevirke Mitre 10":"Mark Jenkins", "D2 Darragh's Mitre 10":"Mark Jenkins", "G11 Gisborne Mitre 10":"Mark Jenkins", "G6 Gore Mitre 10":"Bruce Gasson",
                      "G2A Griffen & Smith Mitre 10":"Bruce Gasson", "G4 Grove Mitre 10":"Ronny Hewson", "H10 Helensville Mitre 10":"Ronny Hewson", "J6M Jacks Mitre 10":"Bruce Gasson", "J10 Jones & Sandford Mitre 10":"Tadak Brejnakowski",
                      "K2 K J Mitre 10":"Mark Jenkins", "K12 Kerikeri Mitre 10":"Ronny Hewson", "K11 Kiwitown Mitre 10":"Mark Jenkins", "L9 Levin Mitre 10":"Bruce Gasson", "M6 Martin Mitre 10":"Bruce Gasson",
                      "M13 Masters Mitre 10":"Tadak Brejnakowski", "M8 Matamata Mitre 10":"Mark Jenkins", "M12 McCarthny Mitre 10":"Ronny Hewson", "X51 Mitre 10 MEGA Albany":"Ronny Hewson", "X16 Mitre 10 MEGA Ashburton":"Bruce Gasson",
                      "X87 Mitre 10 MEGA Botany":"Ronny Hewson", "X28 Mitre 10 MEGA Cambridge":"Mark Jenkins", "X9 Mitre 10 MEGA Dunedin":"Bruce Gasson", "X36 Mitre 10 MEGA Ferrymead":"Bruce Gasson",
                      "X36T Mitre 10 MEGA Ferrymead":"Bruce Gasson", "X12 Mitre 10 MEGA Glenfield":"Ronny Hewson", "X39 Mitre 10 MEGA Greymouth":"Bruce Gasson", "X1 Mitre 10 MEGA Hastings":"Bruce Gasson",
                      "X56 Mitre 10 MEGA Henderson":"Ronny Hewson", "X3 Mitre 10 MEGA Hornby":"Bruce Gasson", "X7 Mitre 10 MEGA Invercargill":"Bruce Gasson", "X30 Mitre 10 MEGA Kapiti":"Bruce Gasson",
                      "X30A Mitre 10 MEGA Kapiti":"Bruce Gasson", "X67 Mitre 10 MEGA Manukau":"Mark Jenkins", "X21 Mitre 10 MEGA Marlborough":"Bruce Gasson", "X25 Mitre 10 MEGA Masterton":"Bruce Gasson",
                      "X88 Mitre 10 MEGA Mt Wellington":"Ronny Hewson", "X17 Mitre 10 MEGA Napier":"Bruce Gasson", "X14 Mitre 10 MEGA Nelson":"Bruce Gasson", "X44 Mitre 10 MEGA New Lynn":"Ronny Hewson",
                      "X18 Mitre 10 MEGA New Plymouth":"Tadak Brejnakowski", "X89 Mitre 10 MEGA Oamaru":"Bruce Gasson", "X49 Mitre 10 MEGA Palmerston North":"Bruce Gasson", "X31 Mitre 10 MEGA Papanui":"Bruce Gasson",
                      "X8 Mitre 10 MEGA Petone":"Bruce Gasson", "X46 Mitre 10 MEGA Porirua":"Bruce Gasson", "X27 Mitre 10 MEGA Pukekohe":"Ronny Hewson", "X52 Mitre 10 MEGA Queenstown":"Bruce Gasson",
                      "X23 Mitre 10 MEGA Rangiora":"Bruce Gasson", "X54 Mitre 10 MEGA Rotorua":"Mark Jenkins", "X53 Mitre 10 MEGA Ruakura":"Mark Jenkins", "X65 Mitre 10 MEGA Silverdale":"Ronny Hewson",
                      "X47 Mitre 10 MEGA Takanini":"Ronny Hewson", "X45 Mitre 10 MEGA Taupo":"Mark Jenkins", "X5 Mitre 10 MEGA Tauranga":"Mark Jenkins", "X32 Mitre 10 MEGA Te Awamutu":"Mark Jenkins",
                      "X11 Mitre 10 MEGA Te Rapa":"Mark Jenkins", "X29 Mitre 10 MEGA Timaru":"Bruce Gasson", "X22 Mitre 10 MEGA Upper Hutt":"Bruce Gasson", "X60 Mitre 10 MEGA Wanaka":"Bruce Gasson",
                      "X50 Mitre 10 MEGA Wanganui":"Bruce Gasson", "X35 Mitre 10 MEGA Warkworth":"Ronny Hewson", "X48 Mitre 10 MEGA Westgate":"Ronny Hewson", "X57 Mitre 10 MEGA Whangarei":"Ronny Hewson",
                      "X49J Mitre10 MEGA Palmerston Nth DC":"Bruce Gasson", "M27 Morrinsville Mitre 10":"Mark Jenkins", "W27 Motueka Mitre 10":"Bruce Gasson", "O5 Opotiki Mitre 10":"Mark Jenkins",
                      "P6 Pain & Kershaw Mitre 10":"Bruce Gasson", "P3 Papamoa Mitre 10":"Mark Jenkins", "5085 Ponsonby Mitre 10":"Ronny Hewson", "S5B Smiths Mitre 10":"Bruce Gasson", "T12 Taumarunui Mitre 10":"Mark Jenkins",
                      "T12 Taumarunui Mitre 10":"Mark Jenkins", "T12T Taumarunui Timber":"Mark Jenkins", "X5D Tauranga Distribution Centre":"Mark Jenkins", "T16 Te Anau Mitre 10":"Bruce Gasson", "T8 Te Kuiti Mitre 10":"Mark Jenkins",
                      "T15 Te Puke Mitre 10":"Mark Jenkins", "T14 Thames Mitre 10":"Mark Jenkins", "M5 Waihi Mitre 10":"Mark Jenkins", "M5T Waihi Mitre 10 Prenail & Truss":"Mark Jenkins", "W31 Waiuku Mitre 10":"Ronny Hewson",
                      "W34 Whakatane Mitre 10":"Mark Jenkins", "W67 Whangaparaoa Mitre 10":"Ronny Hewson", "W12 Winton Mitre 10":"Bruce Gasson"}
    
    data = data[data['National RII'].isin(['A', 'B'])]

    sales_rep_list = []
    
    for i in data['Store']:
      try:
        sales_rep_list.append(sales_rep_dict[i])
      except:
        sales_rep_list.append("")

    data['Sales Rep'] = sales_rep_list
    data['Count'] = 1 * len(data)

    data_item = data.groupby(by=['Supplier Item Code', 'Item Description']).sum()['Count']

    
    st.dataframe(data_item)
    st.dataframe(data)

  except:
    st.error(f"An error occurred: {e}")
