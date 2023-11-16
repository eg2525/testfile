import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
import openpyxl 

def app1():
    # Streamlitアプリのタイトル
    st.title('仕訳インポート')

    # 説明文の追加（Markdown形式）
    st.markdown("""
        ここにアプリの説明文を追加します。
        """)

    # ファイルアップローダー
    uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=['csv', 'xlsx'])

    # アップロードされたファイルがあれば処理を実行
    if uploaded_file is not None:
        try:
            # ファイルの拡張子に基づいて処理を分岐
            if uploaded_file.name.endswith('.csv'):
                # cp932エンコーディングでCSVを読み込む
                df = pd.read_csv(uploaded_file, encoding='cp932')
            elif uploaded_file.name.endswith('.xlsx'):
                # Excelファイルを読み込む
                df = pd.read_excel(uploaded_file)
            
            # データフレームを表示
            st.dataframe(df)

            # 新規Excelファイルの作成とダウンロードリンクの提供
            new_headers = ["日付", "伝票番号", ...]  # ヘッダーのリストを続ける
            new_df = pd.DataFrame(columns=new_headers)
            towrite = BytesIO()
            new_df.to_excel(towrite, index=False, header=True, engine='openpyxl')
            towrite.seek(0)  # ファイルポインタを先頭に戻す
            b64 = base64.b64encode(towrite.read()).decode()  # バイトデータをbase64にエンコード
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="新規データ.xlsx">新規データ.xlsxをダウンロード</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            # ここにエラー処理のコードを追加する

# アプリを実行
app1()
