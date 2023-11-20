import streamlit as st
import pandas as pd
from io import BytesIO
import base64

def app1():
    st.title('仕訳インポート')
    st.markdown("ここにアプリの説明文を追加します。")

    uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        # エラーハンドリングを追加
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='cp932')
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
            return

        # 出力ファイルの固定されたヘッダー
        fixed_headers = ["日付","伝票番号","決算整理仕訳","借方勘定科目","借方科目コード","借方補助科目","借方取引先","借方取引先コード","借方部門","借方品目","借方メモタグ","借方セグメント1","借方セグメント2","借方セグメント3","借方金額","借方税区分","借方税額","貸方勘定科目","貸方科目コード","貸方補助科目","貸方取引先","貸方取引先コード","貸方部門","貸方品目","貸方メモタグ","貸方セグメント1","貸方セグメント2","貸方セグメント3","貸方金額","貸方税区分","貸方税額","摘要"
] 

        # アップロードされたファイルのヘッダーを取得
        uploaded_headers = df.columns.tolist()
        # プルダウン用に「転記しない」オプションを追加
        options = ["転記しない"] + uploaded_headers

        # マッピングの構築
        mappings = {}
        for fixed_header in fixed_headers:
            # 固定ヘッダーに対応するアップロードされたファイルのヘッダーを選択
            mappings[fixed_header] = st.selectbox(f"Select column for: {fixed_header}", options, key=fixed_header)

        # データの転記
        if st.button('OK'):
            new_df = pd.DataFrame()
            for fixed_header in fixed_headers:
                selected_header = mappings[fixed_header]
                if selected_header != "転記しない":
                    new_df[fixed_header] = df[selected_header] if selected_header in uploaded_headers else pd.NA
                else:
                    new_df[fixed_header] = pd.NA

            # Excelファイルのダウンロードリンクを提供
            towrite = BytesIO()
            new_df.to_excel(towrite, index=False)  # engine='openpyxl'は省略可能です
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="仕訳インポート.xlsx">仕訳インポート.xlsxをダウンロード</a>'
            st.markdown(href, unsafe_allow_html=True)

app1()
