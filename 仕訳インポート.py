import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
import openpyxl  # Excelファイルの処理に必要
import base64  # base64エンコーディング用

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

            # 新しいDataFrameを作成
            new_headers = ["日付","伝票番号","決算整理仕訳","借方勘定科目","借方科目コード","借方補助科目","借方取引先","借方取引先コード","借方部門","借方品目","借方メモタグ","借方セグメント1","借方セグメント2","借方セグメント3","借方金額","借方税区分","借方税額","貸方勘定科目","貸方科目コード","貸方補助科目","貸方取引先","貸方取引先コード","貸方部門","貸方品目","貸方メモタグ","貸方セグメント1","貸方セグメント2","貸方セグメント3","貸方金額","貸方税区分","貸方税額","摘要"]  # ヘッダーのリストを続ける
            new_df = pd.DataFrame(columns=new_headers)
            # ここで新しいDataFrameにデータを追加・編集する処理があればここに記述
        
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            # ここにエラー処理のコードを追加する

    # Excelファイルとしてユーザーにダウンロードさせる関数
    def convert_df_to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    # ダウンロードボタンを表示する
    if 'new_df' in locals():
        st.download_button(
            label="新しいExcelファイルをダウンロード",
            data=convert_df_to_excel(new_df),
            file_name='新規データ.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

# アプリを実行
app1()