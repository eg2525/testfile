import streamlit as st
import pandas as pd

st.title('test_code')

# ファイルのアップロード
uploaded_files = st.file_uploader("日計報告を全てアップロードしてください", accept_multiple_files=True, type=['xlsm'])

# 月のリスト
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

# ユーザーから月を選択してもらう
selected_month = st.selectbox("読み込むシート名を選択してください:", months)

# チェックボックスで処理開始
if st.checkbox('処理開始'):
    if uploaded_files and selected_month:
        dataframes = {}

        for uploaded_file in uploaded_files:
            df = pd.read_excel(uploaded_file, sheet_name=selected_month, header=7)
            df.columns = [col.replace('\n', '') for col in df.columns]
            dataframes[uploaded_file.name] = df

        columns = ["つくば", "羽生", "王子", "三鷹", "仙台", "川口", "船橋", "南森町", "高田馬場", "横浜関内", "福岡天神", "大宮"]
        index = ["自費", "社保", "国保", "販売品", "過不足金", "保険返金", "その他/保険証忘れ", "売上合計", "窓口現金", "窓口クレジット", "窓口合計", "精算機現金", "精算機クレジット", "取消し", "精算機合計", "振込入金", "自費返金", "JACCS入金", "口座振替", "[点]後期高齢", "[点]国保窓口入金", "[点]社保窓口入金", "[点]合計", "[一・負]後期高齢", "[一・負]国保窓口入金", "[一・負]社保窓口入金", "[一・負]合計", "差額"]
        
        final_df = pd.DataFrame(index=index, columns=columns)
        for filename, data in dataframes.items():
            for column in columns:
                if column in filename:
                    for idx in index:
                        clean_index = idx.replace(' ', '')
                        if clean_index in data.columns:
                            value = data[clean_index].iloc[31] if len(data[clean_index]) > 31 else None
                            final_df.at[idx, column] = value

        if st.button("変更を保存"):
            # 新しいDataFrameのカラムを定義
            output_columns = ['収支区分', '発生日', '取引先', '税区分', '勘定科目', '品目', '部門', '金額']
            # 空のDataFrameを作成
            output_df = pd.DataFrame(columns=output_columns)

            # final_dfからoutput_dfへのデータ転記
            for col in final_df.columns:
                for idx in final_df.index:
                    value = final_df.at[idx, col]
                    if value != 0 and value is not None:  # セルの値が0でもNoneでもない場合に転記
                        new_row = pd.DataFrame({
                            '品目': [idx],
                            '部門': [col],
                            '金額': [value]
                        }, columns=output_columns)
                        output_df = pd.concat([output_df, new_row], ignore_index=True)  # 新しい行をDataFrameに追加

            st.success('変更がfinal_dfに保存され、データがoutput_dfに転記されました。')
            st.write(output_df)  # 最終的なDataFrameを表示
