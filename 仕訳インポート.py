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
        output_headers = ["日付", "伝票番号", "..."]  # ここには実際の出力ヘッダーをリストとして追加します
        output_headers_with_option = ["転記しない"] + output_headers

        # ヘッダーとプルダウンを横に並べて表示
        mappings = {}
        for header in uploaded_headers:
            col1, col2 = st.columns([3, 2])  # 2列レイアウトを作成
            with col1:
                st.text(header)
            with col2:
                # デフォルトで「転記しない」が選択されているようにする
                mappings[header] = st.selectbox(f"{header} に対応するヘッダー:", options=output_headers_with_option, index=0)

        if st.button('OK'):
            # マッピングに基づいてデータを新しいDataFrameに転記
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
