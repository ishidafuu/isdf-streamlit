import anthropic
import streamlit as st

from fins_statements import call_fins_statements


class ChatApp:
    def __init__(self, anthropic_key, id_token):
        self.anthropic_key = anthropic_key
        self.messages = []
        self.model_options = ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]
        self.model = self.model_options[0]
        self.id_token = id_token
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

        # 財務情報の取得とClaude-3への渡し方
        if stock_code:
            # 財務情報APIを呼び出す（この部分は実際のAPIによって異なります）
            financial_data = self.get_financial_data(stock_code)

            # プロンプトのテキストを読み込む
            with open("prompt.txt", "r", encoding="utf-8") as f:
                prompt = f.read().format(financial_data=financial_data)

            print(prompt)
            # 財務情報をClaude-3に渡す
            self.messages.append({"role": "user", "content": f"{prompt}"})

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
    def get_financial_data(self, stock_code):
        # APIを呼び出して応答を取得
        response = call_fins_statements(self.id_token, stock_code)

        # 応答からデータを抽出
        financial_data = response.to_dict()

        return financial_data
