import unittest.mock

from fins_statements import call_fins_statements
from token_manager import TokenManager

"""
j-QuantsAPIにて各種株式情報を取得する。
"""


class TestGetQuantsData(unittest.TestCase):

    def test_api_fins_statements(self):
        # 銘柄コードの設定
        stock_code = '2330'
        id_token = TokenManager().get_id_token_local()
        response = call_fins_statements(id_token, stock_code)

        df = response.to_dataframe_income()
        with open(f"to_dataframe_income{stock_code}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            csvfile.write(df.to_csv())

        df = response.to_dataframe_balance()
        with open(f"to_dataframe_balance{stock_code}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            csvfile.write(df.to_csv())

        df = response.to_dataframe_cashflow()
        with open(f"to_dataframe_cashflow{stock_code}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            csvfile.write(df.to_csv())

        df = response.to_dataFrame_quarter_grow()
        with open(f"to_dataFrame_quarter_grow{stock_code}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            csvfile.write(df.to_csv())


if __name__ == '__main__':
    # テストの実行
    unittest.main()
