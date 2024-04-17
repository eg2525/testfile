import streamlit as st
import pandas as pd

columns = ["つくば", "羽生", "王子", "三鷹", "仙台", "川口", "船橋", "南森町", "高田馬場", "横浜関内", "福岡天神", "大宮"]
index = ['後期高齢', '国保窓口入金', '社保窓口入金']

# 空のDataFrameを作成
df = pd.DataFrame(index=index, columns=columns)

edited_df = st.data_editor(df)
