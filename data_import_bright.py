import streamlit as st
import pandas as pd

st.title('test_code')

# ファイルのアップロード
uploaded_files = st.file_uploader("日計報告を全てアップロードしてください", accept_multiple_files=True, type=['xlsm'])

# 月のリスト
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

# ユーザーから月を選択してもらう
selected_month = st.selectbox("読み込むシート名を選択してください:", months)

# 処理開始のチェックボックスがチェックされ、ファイルがアップロードされ、処理が完了した後にデータフレームを表示
if st.checkbox('処理開始'):
    if uploaded_files and selected_month:
        dataframes = {}

        for uploaded_file in uploaded_files:
            df = pd.read_excel(uploaded_file, sheet_name=selected_month, header=7)
            df.columns = [col.replace('\n', '') for col in df.columns]
            dataframes[uploaded_file.name] = df

        columns = ["つくば", "羽生", "王子", "三鷹", "仙台", "川口", "船橋", "南森町", "高田馬場", "横浜関内", "福岡天神", "大宮"]
        index = ["自費", "社保", "国保", "販売品", "過不足金", "保険返金", "その他/保険証忘れ", "売上合計", "窓口現金", "窓口クレジット", "窓口合計", "精算機現金", "精算機クレジット", "取消し", "精算機合計", "振込入金", "自費返金", "JACCS入金", "口座振替"]
        
        final_df = pd.DataFrame(index=index, columns=columns)
        for filename, data in dataframes.items():
            for column in columns:
                if column in filename:
                    for idx in index:
                        if idx == '口座振替':
                            # 口座振替は特定のセルから値を取得します
                            if data.shape[0] > 35 and data.shape[1] > 6:  # セルの位置が存在するかチェック
                                value = data.iloc[35, 6]  # 0-indexedでH44の値を取得
                            else:
                                value = None
                        else:
                            clean_index = idx.replace(' ', '')
                            if clean_index in data.columns:
                                value = data[clean_index].iloc[31] if len(data[clean_index]) > 31 else None
                        
                        final_df.at[idx, column] = value

        # ここでデータフレームを表示します
        st.dataframe(final_df)
