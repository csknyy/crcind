import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="Item volume check", layout="wide")

uploaded_file = st.file_uploader("Choose the .xlsx file")

if uploaded_file is not None:
    try:
        data = pd.read_excel(uploaded_file, header=0, engine='openpyxl')

        new_headers1 = [str(i)[:4] for i in data.columns.copy()]
        new_headers2 = [str(i) for i in data.iloc[0, :].copy()]
        new_headers = ['-'.join([i, j]) for i, j in zip(new_headers1, new_headers2)]
        
        data.columns = new_headers
        data = data[[col for col in data.columns if not col.endswith('Total')]]
        data = data.drop(data.index[:2])
        data = data.drop(data.index[-3:])
        data = data.iloc[:, :-2]
        data = data.reset_index(drop=True)
        data.columns.values[0] = 'Legacy Item Number'
        data = data.fillna(0)

        data_CY = data.iloc[:, [0] + list(range(-6, 0))].copy()
        data_CY.iloc[:, -6:] = data_CY.iloc[:, -6:].astype(int)
        data_CY.loc[:, 'CY_total'] = data_CY.iloc[:, -6:].sum(axis=1).astype(int)
        data_CY['CY_count'] = data_CY.iloc[:, -7:-1].apply(lambda row: (row != 0).sum(), axis=1)
        data_CY['CY_last_month_weight'] = np.where(data_CY['CY_total'] != 0, data_CY.iloc[:, -3] / data_CY['CY_total'], 0)

        data_PY = data.iloc[:, [0] + list(range(-18, -12))].copy()
        data_PY.iloc[:, -6:] = data_PY.iloc[:, -6:].astype(int)
        data_PY.loc[:, 'PY_total'] = data_PY.iloc[:, -6:].sum(axis=1).astype(int)
        data_PY['PY_count'] = data_PY.iloc[:, -7:-1].apply(lambda row: (row != 0).sum(), axis=1)
        data_PY['PY_last_month_weight'] = np.where(data_PY['PY_total'] != 0, data_PY.iloc[:, -3] / data_PY['PY_total'], 0)

        merged_data = pd.merge(data_PY, data_CY, on='Legacy Item Number', how='left')
        merged_data['Weight_variance'] = merged_data['CY_last_month_weight'] - merged_data['PY_last_month_weight']

        merged_data = merged_data.sort_values(by='CY_total', ascending=False).reset_index(drop=True)

        up1, up2, up3, up4 = st.columns(4)
        with up1:
            text_up1 = st.text_input('Greater weight than',value=0.22)
            text_up1 = float(text_up1)
        with up2:
            text_up2 = st.text_input('Difference between PY weight',value=0.05)
            text_up2 = float(text_up2)
        with up3:
            text_up3 = st.text_input('Months with sales (at least)',value=1)
            text_up3 = int(text_up3)
        with up4:
            text_up4 = st.text_input('Total 6 month qty more than',value=50)
            text_up4 = int(text_up4)
        
        filter_up1 = (merged_data['CY_last_month_weight'] > text_up1)
        filter_up2 = (merged_data['Weight_variance'] > text_up2)
        filter_up3 = (merged_data['CY_count'] >= text_up3)
        filter_up4 = (merged_data['CY_total'] > text_up4)

        going_up = merged_data[filter_up1 & filter_up2 & filter_up3 & filter_up4].reset_index(drop=True)
        going_up = going_up.iloc[:,[0,6,7,9,15,16,18,19]]

        filter_down1 = (merged_data['CY_last_month_weight'] < 0.10)
        filter_down2 = (merged_data['Weight_variance'] < -0.05)
        filter_down3 = (merged_data['CY_count'] > 0)
        filter_down4 = (merged_data['CY_total'] > 50)

        going_down = merged_data[filter_down1 & filter_down2 & filter_down3 & filter_down4].reset_index(drop=True)
        going_down = going_down.iloc[:,[0,6,7,9,15,16,18,19]]

        st.dataframe(going_up)
        st.dataframe(going_down)

    except Exception as e:
        st.error(f"Error: {e}")
