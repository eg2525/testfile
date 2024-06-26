import streamlit as st
import pandas as pd

st.title('test_code')

index = ["つくば", "羽生", "王子", "三鷹", "仙台", "川口", "船橋", "南森町", "高田馬場", "横浜関内", "福岡天神", "大宮"]
columns = ['社保窓口入金', '国保窓口入金', '後期高齢']

# 空のDataFrameを作成
df = pd.DataFrame(index=index, columns=columns)

# 編集用のデータエディタを配置
edited_df = st.data_editor(df)

# 出力用DataFrameの列を定義
output_columns = ['収支区分', '発生日', '取引先', '税区分', '勘定科目', '品目', '部門', '金額']
output_df = pd.DataFrame(columns=output_columns)

selected_date = st.date_input("発生日を選択してください:", value=pd.to_datetime("today"))

if st.checkbox("OK"):
    df.update(edited_df, overwrite=True)
    df = df.applymap(lambda x: pd.to_numeric(x, errors='ignore'))
    df = df.applymap(lambda x: x * 7 if pd.notna(x) and isinstance(x, (int, float)) else x)

    df['国保'] = df['国保窓口入金'] + df['後期高齢']
    df.drop(['国保窓口入金', '後期高齢'], axis=1, inplace=True)
    df.rename(columns={'社保窓口入金': '社保'}, inplace=True)

    # dfの値をoutput_dfに移す
    for col in df.columns:
        for idx in df.index:
            value = df.at[idx, col]

            # 空文字やNaNをNoneに統一し、数値型に変換を試みる
            if pd.isna(value):
                value = None
            else:
                try:
                    # 数値型への強制変換を試みる
                    value = float(value)
                except ValueError:
                    continue  # 数値に変換できない場合はスキップ

            # Noneまたは0ではない場合に転記
            if value is not None and value != 0:
                new_row = pd.DataFrame({'収支区分': ['収入'], '発生日': [''], '取引先': [selected_date], '税区分': ['非課売上'], '勘定科目': ['保険診療収入'], '品目': [col], '部門': [idx], '金額': [value]}, columns=output_columns)
                output_df = pd.concat([output_df, new_row], ignore_index=True)

    # 結果のDataFrameを表示
    st.write(output_df)

    # CSVファイルとしてダウンロードするためのリンクを作成
    @st.cache
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('cp932')

    csv_data = convert_df_to_csv(output_df)
    st.download_button(
        label="Download data as CSV",
        data=csv_data,
        file_name='import_data(請求).csv',
        mime='text/csv',
    )