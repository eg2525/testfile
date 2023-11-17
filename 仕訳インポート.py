import streamlit as st
import pandas as pd
from io import BytesIO
import base64

def app1():
    st.title('仕訳インポート')
    st.markdown("ここにアプリの説明文を追加します。")

    uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='cp932')
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        # 出力ファイルの固定されたヘッダー
        fixed_headers = ["日付","伝票番号","決算整理仕訳","借方勘定科目","借方科目コード","借方補助科目","借方取引先","借方取引先コード","借方部門","借方品目","借方メモタグ","借方セグメント1","借方セグメント2","借方セグメント3","借方金額","借方税区分","借方税額","貸方勘定科目","貸方科目コード","貸方補助科目","貸方取引先","貸方取引先コード","貸方部門","貸方品目","貸方メモタグ","貸方セグメント1","貸方セグメント2","貸方セグメント3","貸方金額","貸方税区分","貸方税額","摘要"
]  # 全部のヘッダーをここに追加
        # ヘッダーのマッピングを設定するためのプルダウンメニューを生成
        header_mapping = {fh: st.selectbox(f"{fh}:", [""] + list(df.columns), index=0) for fh in fixed_headers}
        
        if st.button('OK'):
            # マッピングに基づいてデータを新しいDataFrameに転記
            new_df = pd.DataFrame(columns=fixed_headers)
            for fh in fixed_headers:
                if header_mapping[fh]:  # 空文字列でない場合にのみ転記
                    new_df[fh] = df[header_mapping[fh]]
                else:
                    new_df[fh] = ""  # 空文字列で初期化

            # Excelファイルのダウンロードリンクを提供
            towrite = BytesIO()
            new_df.to_excel(towrite, index=False)  # engine='openpyxl'は省略可能です
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="新規データ.xlsx">新規データ.xlsxをダウンロード</a>'
            st.markdown(href, unsafe_allow_html=True)

app1()
