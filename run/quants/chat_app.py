import anthropic
import pandas
import streamlit as st

from common import GCSUploader
from fins_statements import call_fins_statements, FinsStatementsResult


class ChatApp:
    def __init__(self, anthropic_key: str, id_token: str, is_local: bool):
        self.anthropic_key = anthropic_key
        self.messages = []
        self.model_options = ["claude-3-sonnet-20240229"]
        # self.model_options = ["claude-3-sonnet-20240229", "claude-3-opus-20240229"]
        # self.model_options = ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]
        self.model = self.model_options[0]
        self.id_token = id_token
        self.is_local = is_local
        self.financial_data = None  # 財務情報を格納する変数

    def start_chat(self):
        with st.sidebar:
            self.model = st.radio("Select a model", self.model_options, index=self.model_options.index(self.model))

        # AntrhopicClientを初期化
        client = anthropic.Anthropic(api_key=self.anthropic_key)

        # タイトルを設定
        st.title(f"{self.model}")

        # 銘柄コードの入力フィールドを追加
        stock_code = st.text_input("Enter a stock code")

        # プロンプトのテキストを読み込む
        with open("prompt.txt", "r", encoding="utf-8") as f:
            default_prompt = f.read()

        prompt = st.text_area("プロンプト {financial_data}:財務情報", default_prompt, height=400)

        # 財務情報の取得とClaude-3への渡し方
        if stock_code:
            # 財務情報APIを呼び出す（この部分は実際のAPIによって異なります）
            financial_data = self.get_financial_data(stock_code)

            income_data = financial_data.to_dataframe_income().to_csv()
            balance_data = financial_data.to_dataframe_balance().to_csv()
            cashflow_data = financial_data.to_dataframe_cashflow().to_csv()
            quarter_grow_data = financial_data.to_dataFrame_quarter_grow().to_csv()
            # uploader = GCSUploader(self.is_local)
            # blob_name = f"{stock_code}/financial_data.csv"
            # uploader.upload_string(blob_name, financial_data_csv)
            # financial_data_url = f"https://storage.googleapis.com/isdf-quants/{blob_name}"

            # print(financial_data)
            # 財務情報をClaude-3に渡す
            self.messages.append({"role": "user", "content": f"{prompt.format(income_data=income_data, balance_data=balance_data, cashflow_data=cashflow_data, quarter_grow_data=quarter_grow_data)}"})

            # Claude-3に銘柄判断を求める
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response_message = ""
                with client.messages.stream(
                        model=self.model,
                        max_tokens=4096,
                        messages=self.messages
                ) as stream:
                    for text in stream.text_stream:
                        response_message += text
                        message_placeholder.markdown(response_message)

            final_message = stream.get_final_message()
            input_token = final_message.usage.input_tokens
            output_token = final_message.usage.output_tokens
            message_placeholder.markdown(f"{response_message} \n token:{input_token + output_token} (i:{input_token} o:{output_token})")
            self.messages.append({"role": "assistant", "content": response_message})

    # 財務情報APIを呼び出す関数（実際のAPIによって異なります）
    def get_financial_data(self, stock_code) -> FinsStatementsResult:
        # APIを呼び出して応答を取得
        response = call_fins_statements(self.id_token, stock_code)
        # df = response.to_dataFrame_sales()
        # with open(f"fins_{stock_code}.csv", 'w', newline='', encoding='utf-8') as csvfile:
        #     csvfile.write(df.to_csv())

        # df = response.to_dataFrame_quarter_grow()
        # with open(f"fins_qg_{stock_code}.csv", 'w', newline='', encoding='utf-8') as csvfile:
        #     csvfile.write(df.to_csv())

        return response
