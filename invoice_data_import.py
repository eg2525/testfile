import streamlit as st
import pandas as pd

st.title('test_code')

index = ["つくば", "羽生", "王子", "三鷹", "仙台", "川口", "船橋", "南森町", "高田馬場", "横浜関内", "福岡天神", "大宮"]
columns = ['社保窓口入金', '国保窓口入金', '後期高齢']

# 空のDataFrameを作成
df = pd.DataFrame(index=index, columns=columns)

edited_df = st.data_editor(df)

if st.checkbox("OK"):
    output_columns = ['収支区分', '発生日', '取引先', '税区分', '勘定科目', '品目', '部門', '金額']
    output_df = pd.DataFrame(columns=output_columns)

