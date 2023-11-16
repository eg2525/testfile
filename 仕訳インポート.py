import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl

def app1():
    st.title('仕訳インポート')
    st.markdown("ここにアプリの説明文を追加します。")

    uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='cp932')
        else:
            df = pd.read_excel(uploaded_file)

        uploaded_headers = df.columns.tolist()
        output_headers = ["日付","伝票番号","決算整理仕訳","借方勘定科目","借方科目コード","借方補助科目","借方取引先","借方取引先コード","借方部門","借方品目","借方メモタグ","借方セグメント1","借方セグメント2","借方セグメント3","借方金額","借方税区分","借方税額","貸方勘定科目","貸方科目コード","貸方補助科目","貸方取引先","貸方取引先コード","貸方部門","貸方品目","貸方メモタグ","貸方セグメント1","貸方セグメント2","貸方セグメント3","貸方金額","貸方税区分","貸方税額","摘要"]  # 出力ファイルのヘッダーリスト
        output_headers_with_option = ["転記しない"] + output_headers  # プルダウン用に「転記しない」オプションを追加

        mappings = {}
        for header in uploaded_headers:
            col1, col2 = st.columns([3, 2])  # 2列レイアウトを作成
            with col1:
                st.text(header)
            with col2:
                mappings[header] = st.selectbox("", output_headers_with_option, key=header)

        if st.button('OK'):
            new_df = pd.DataFrame()
            for in_header, out_header in mappings.items():
                if out_header != "転記しない":  # 「転記しない」が選択されていない場合に転記
                    new_df[out_header] = df[in_header]

            # 新しいDataFrameをExcelファイルに変換してダウンロードリンクを提供
            towrite = BytesIO()
            new_df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="新規データ.xlsx">新規データ.xlsxをダウンロード</a>'
            st.markdown(href, unsafe_allow_html=True)

app1()
