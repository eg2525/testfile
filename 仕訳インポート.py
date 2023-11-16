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
        new_headers = ["日付","伝票番号","決算整理仕訳","借方勘定科目","借方科目コード","借方補助科目","借方取引先","借方取引先コード","借方部門","借方品目","借方メモタグ","借方セグメント1","借方セグメント2","借方セグメント3","借方金額","借方税区分","借方税額","貸方勘定科目","貸方科目コード","貸方補助科目","貸方取引先","貸方取引先コード","貸方部門","貸方品目","貸方メモタグ","貸方セグメント1","貸方セグメント2","貸方セグメント3","貸方金額","貸方税区分","貸方税額","摘要"]  # 出力ファイルのヘッダーリスト
        new_headers_with_option = new_headers + ["転記しない"]  # プルダウン用に「転記しない」オプションを追加

        mappings = {}
        for header in uploaded_headers:
            col1, col2 = st.columns(2)
            with col1:
                st.text(header)
            with col2:
                selected_header = st.selectbox("→", new_headers_with_option, key=header)
            mappings[header] = selected_header

        if st.button('OK'):
            new_df = pd.DataFrame()
            for in_header, out_header in mappings.items():
                if out_header in new_headers:  # 「転記しない」以外の場合に転記
                    new_df[out_header] = df[in_header]

            # ここで新しいDataFrameをExcelファイルに変換してダウンロードリンクを提供

app1()
