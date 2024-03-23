import csv
import io
from datetime import datetime
from typing import List, Optional

import pandas as pd
import requests
from pydantic import BaseModel


class Statement(BaseModel):
    # 開示日
    DisclosedDate: str
    # 開示時刻
    DisclosedTime: str
    # 銘柄コード（5桁）
    LocalCode: str
    # 開示番号
    DisclosureNumber: str
    # 開示書類種別
    TypeOfDocument: str
    # 当会計期間の種類（[1Q, 2Q, 3Q, 4Q, FY]）
    TypeOfCurrentPeriod: str
    # 当会計期間開始日
    CurrentPeriodStartDate: str
    # 当会計期間終了日
    CurrentPeriodEndDate: str
    # 当事業年度開始日
    CurrentFiscalYearStartDate: str
    # 当事業年度終了日
    CurrentFiscalYearEndDate: str
    # 翌事業年度開始日
    NextFiscalYearStartDate: Optional[str]
    # 翌事業年度終了日
    NextFiscalYearEndDate: Optional[str]
    # 売上高
    NetSales: str
    # 営業利益
    OperatingProfit: str
    # 経常利益
    OrdinaryProfit: str
    # 当期純利益
    Profit: str
    # 一株あたり当期純利益
    EarningsPerShare: str
    # 潜在株式調整後一株あたり当期純利益
    DilutedEarningsPerShare: str
    # 総資産
    TotalAssets: str
    # 純資産
    Equity: str
    # 自己資本比率
    EquityToAssetRatio: str
    # 一株あたり純資産
    BookValuePerShare: str
    # 営業活動によるキャッシュ・フロー
    CashFlowsFromOperatingActivities: str
    # 投資活動によるキャッシュ・フロー
    CashFlowsFromInvestingActivities: str
    # 財務活動によるキャッシュ・フロー
    CashFlowsFromFinancingActivities: str
    # 現金及び現金同等物期末残高
    CashAndEquivalents: str
    # 一株あたり配当実績_第1四半期末
    ResultDividendPerShare1stQuarter: str
    # 一株あたり配当実績_第2四半期末
    ResultDividendPerShare2ndQuarter: str
    # 一株あたり配当実績_第3四半期末
    ResultDividendPerShare3rdQuarter: str
    # 一株あたり配当実績_期末
    ResultDividendPerShareFiscalYearEnd: str
    # 一株あたり配当実績_合計
    ResultDividendPerShareAnnual: str
    # 1口当たり分配金（REIT）
    DistributionsPerUnit: Optional[str] = None
    # 配当金総額
    ResultTotalDividendPaidAnnual: str
    # 配当性向
    ResultPayoutRatioAnnual: str
    # 一株あたり配当予想_第1四半期末
    ForecastDividendPerShare1stQuarter: str
    # 一株あたり配当予想_第2四半期末
    ForecastDividendPerShare2ndQuarter: str
    # 一株あたり配当予想_第3四半期末
    ForecastDividendPerShare3rdQuarter: str
    # 一株あたり配当予想_期末
    ForecastDividendPerShareFiscalYearEnd: str
    # 一株あたり配当予想_合計
    ForecastDividendPerShareAnnual: str
    # 1口当たり予想分配金（REIT）
    ForecastDistributionsPerUnit: Optional[str] = None
    # 予想配当金総額
    ForecastTotalDividendPaidAnnual: str
    # 予想配当性向
    ForecastPayoutRatioAnnual: str
    # 一株あたり配当予想_翌事業年度第1四半期末
    NextYearForecastDividendPerShare1stQuarter: str
    # 一株あたり配当予想_翌事業年度第2四半期末
    NextYearForecastDividendPerShare2ndQuarter: str
    # 一株あたり配当予想_翌事業年度第3四半期末
    NextYearForecastDividendPerShare3rdQuarter: str
    # 一株あたり配当予想_翌事業年度期末
    NextYearForecastDividendPerShareFiscalYearEnd: str
    # 一株あたり配当予想_翌事業年度合計
    NextYearForecastDividendPerShareAnnual: str
    # 一口当たり翌事業年度予想分配金（REIT）
    NextYearForecastDistributionsPerUnit: Optional[str] = None
    # 翌事業年度予想配当性向
    NextYearForecastPayoutRatioAnnual: str
    # 売上高_予想_第2四半期末
    ForecastNetSales2ndQuarter: str
    # 営業利益_予想_第2四半期末
    ForecastOperatingProfit2ndQuarter: str
    # 経常利益_予想_第2四半期末
    ForecastOrdinaryProfit2ndQuarter: str
    # 当期純利益_予想_第2四半期末
    ForecastProfit2ndQuarter: str
    # 一株あたり当期純利益_予想_第2四半期末
    ForecastEarningsPerShare2ndQuarter: str
    # 売上高_予想_翌事業年度第2四半期末
    NextYearForecastNetSales2ndQuarter: str
    # 営業利益_予想_翌事業年度第2四半期末
    NextYearForecastOperatingProfit2ndQuarter: str
    # 経常利益_予想_翌事業年度第2四半期末
    NextYearForecastOrdinaryProfit2ndQuarter: str
    # 当期純利益_予想_翌事業年度第2四半期末
    NextYearForecastProfit2ndQuarter: str
    # 一株あたり当期純利益_予想_翌事業年度第2四半期末
    NextYearForecastEarningsPerShare2ndQuarter: str
    # 売上高_予想_期末
    ForecastNetSales: str
    # 営業利益_予想_期末
    ForecastOperatingProfit: str
    # 経常利益_予想_期末
    ForecastOrdinaryProfit: str
    # 当期純利益_予想_期末
    ForecastProfit: str
    # 一株あたり当期純利益_予想_期末
    ForecastEarningsPerShare: str
    # 売上高_予想_翌事業年度期末
    NextYearForecastNetSales: str
    # 営業利益_予想_翌事業年度期末
    NextYearForecastOperatingProfit: str
    # 経常利益_予想_翌事業年度期末
    NextYearForecastOrdinaryProfit: str
    # 当期純利益_予想_翌事業年度期末
    NextYearForecastProfit: str
    # 一株あたり当期純利益_予想_翌事業年度期末
    NextYearForecastEarningsPerShare: str
    # 期中における重要な子会社の異動
    MaterialChangesInSubsidiaries: str
    # 会計基準等の改正に伴う会計方針の変更
    ChangesBasedOnRevisionsOfAccountingStandard: str
    # 会計基準等の改正に伴う変更以外の会計方針の変更
    ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard: str
    # 会計上の見積りの変更
    ChangesInAccountingEstimates: str
    # 修正再表示
    RetrospectiveRestatement: str
    # 期末発行済株式数
    NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock: str
    # 期末自己株式数
    NumberOfTreasuryStockAtTheEndOfFiscalYear: str
    # 期中平均株式数
    AverageNumberOfShares: str
    # 売上高_非連結
    NonConsolidatedNetSales: str
    # 営業利益_非連結
    NonConsolidatedOperatingProfit: str
    # 経常利益_非連結
    NonConsolidatedOrdinaryProfit: str
    # 当期純利益_非連結
    NonConsolidatedProfit: str
    # 一株あたり当期純利益_非連結
    NonConsolidatedEarningsPerShare: str
    # 総資産_非連結
    NonConsolidatedTotalAssets: str
    # 純資産_非連結
    NonConsolidatedEquity: str
    # 自己資本比率_非連結
    NonConsolidatedEquityToAssetRatio: str
    # 一株あたり純資産_非連結
    NonConsolidatedBookValuePerShare: str
    # 売上高_予想_第2四半期末_非連結
    ForecastNonConsolidatedNetSales2ndQuarter: str
    # 営業利益_予想_第2四半期末_非連結
    ForecastNonConsolidatedOperatingProfit2ndQuarter: str
    # 経常利益_予想_第2四半期末_非連結
    ForecastNonConsolidatedOrdinaryProfit2ndQuarter: str
    # 当期純利益_予想_第2四半期末_非連結
    ForecastNonConsolidatedProfit2ndQuarter: str
    # 一株あたり当期純利益_予想_第2四半期末_非連結
    ForecastNonConsolidatedEarningsPerShare2ndQuarter: str
    # 売上高_予想_翌事業年度第2四半期末_非連結
    NextYearForecastNonConsolidatedNetSales2ndQuarter: str
    # 営業利益_予想_翌事業年度第2四半期末_非連結
    NextYearForecastNonConsolidatedOperatingProfit2ndQuarter: str
    # 経常利益_予想_翌事業年度第2四半期末_非連結
    NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter: str
    # 当期純利益_予想_翌事業年度第2四半期末_非連結
    NextYearForecastNonConsolidatedProfit2ndQuarter: str
    # 一株あたり当期純利益_予想_翌事業年度第2四半期末_非連結
    NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter: str
    # 売上高_予想_期末_非連結
    ForecastNonConsolidatedNetSales: str
    # 営業利益_予想_期末_非連結
    ForecastNonConsolidatedOperatingProfit: str
    # 経常利益_予想_期末_非連結
    ForecastNonConsolidatedOrdinaryProfit: str
    # 当期純利益_予想_期末_非連結
    ForecastNonConsolidatedProfit: str
    # 一株あたり当期純利益_予想_期末_非連結
    ForecastNonConsolidatedEarningsPerShare: str
    # 売上高_予想_翌事業年度期末_非連結
    NextYearForecastNonConsolidatedNetSales: str
    # 営業利益_予想_翌事業年度期末_非連結
    NextYearForecastNonConsolidatedOperatingProfit: str
    # 経常利益_予想_翌事業年度期末_非連結
    NextYearForecastNonConsolidatedOrdinaryProfit: str
    # 当期純利益_予想_翌事業年度期末_非連結
    NextYearForecastNonConsolidatedProfit: str
    # 一株あたり当期純利益_予想_翌事業年度期末_非連結
    NextYearForecastNonConsolidatedEarningsPerShare: str

    def to_dict(self):
        return self.dict()

    def to_dict_for_pandas(self):
        d = self.__dict__.copy()
        for k, v in d.items():
            if v == '':
                d[k] = None
        return d


class FinsStatementsResponse(BaseModel):
    statements: List[Statement]
    pagination_key: Optional[str] = None


class FinsStatementsResult:
    def __init__(self, response: FinsStatementsResponse):
        self.statements = response.statements
        self.pagination_key = response.pagination_key

    def get_most_recent_valid_shares(self) -> int:
        valid_statements = [s for s in self.statements if s.NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return int(recent_statement.NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock)
        return 0

    def get_most_recent_earnings_per_share(self) -> float:
        valid_statements = [s for s in self.statements if s.EarningsPerShare not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return float(recent_statement.EarningsPerShare)
        return 0.0

    def get_most_recent_book_value_per_share(self) -> float:
        valid_statements = [s for s in self.statements if s.BookValuePerShare not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return float(recent_statement.BookValuePerShare)
        return 0.0

    def get_most_recent_forecast_dividend_per_share_annual(self) -> float:
        valid_statements = [s for s in self.statements if s.ForecastDividendPerShareAnnual not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return float(recent_statement.ForecastDividendPerShareAnnual)
        return 0.0

    def get_most_recent_equity(self) -> int:
        valid_statements = [s for s in self.statements if s.Equity not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return int(recent_statement.Equity)
        return 0

    def get_most_recent_profit(self) -> int:
        valid_statements = [s for s in self.statements if s.Profit not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return int(recent_statement.Profit)
        return 0

    def get_most_recent_cash_flows_from_operating_activities(self) -> int:
        valid_statements = [s for s in self.statements if s.CashFlowsFromOperatingActivities not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return int(recent_statement.CashFlowsFromOperatingActivities)
        return 0

    def get_most_recent_cash_flows_from_investing_activities(self) -> int:
        valid_statements = [s for s in self.statements if s.CashFlowsFromInvestingActivities not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return int(recent_statement.CashFlowsFromInvestingActivities)
        return 0

    def get_most_recent_cash_flows_from_financing_activities(self) -> int:
        valid_statements = [s for s in self.statements if s.CashFlowsFromFinancingActivities not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return int(recent_statement.CashFlowsFromFinancingActivities)
        return 0

    def get_most_recent_cash_and_equivalents(self) -> int:
        valid_statements = [s for s in self.statements if s.CashAndEquivalents not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return int(recent_statement.CashAndEquivalents)
        return 0

    def get_most_recent_equity_to_asset_ratio(self) -> float:
        valid_statements = [s for s in self.statements if s.EquityToAssetRatio not in [None, ""]]
        if valid_statements:
            recent_statement = max(valid_statements, key=lambda s: datetime.strptime(s.DisclosedDate, '%Y-%m-%d'))
            return float(recent_statement.EquityToAssetRatio)
        return 0.0

    def to_dict(self):
        statements_dict = []
        for s in self.statements:
            statement_dict = s.dict()
            statement_dict = {k: v for k, v in statement_dict.items() if v not in ["", None]}
            statements_dict.append(statement_dict)
        result = {"statements": statements_dict}
        if self.pagination_key not in ["", None]:
            result["pagination_key"] = self.pagination_key
        return result

    def to_dataFrame(self) -> pd.DataFrame:
        df = pd.DataFrame([stmt.to_dict_for_pandas() for stmt in self.statements])
        df = df.dropna(axis=1, how='all')
        # "Revision"を含む行を削除
        df = df[~df['TypeOfDocument'].str.contains('Revision', na=False)]
        with open("fins.csv", 'w', newline='', encoding='utf-8') as csvfile:
            csvfile.write(df.to_csv())
        return df

    def to_csv_string(self) -> str:
        field_names = Statement.__annotations__.keys()
        output = io.StringIO()
        with output:
            writer = csv.DictWriter(output, fieldnames=field_names)
            writer.writeheader()
            for statement in self.statements:
                writer.writerow(statement.to_dict())
            csv_content = output.getvalue()

        # with open("fins.csv", 'w', newline='', encoding='utf-8') as csvfile:
        #     csvfile.write(csv_content)

        return csv_content


def call_fins_statements(token: str, code: str) -> FinsStatementsResult:
    headers = {"Authorization": "Bearer " + token}
    url = "https://api.jquants.com/v1/fins/statements"
    params = {"code": code}

    res = requests.get(url, params=params, headers=headers)

    if res.status_code != 200:
        res_json = res.json()
        message = res_json.get('message', 'No error message returned')
        raise RuntimeError(f"{url}:{params}:{message}")

    # 株情報をパースしてリストに追加
    fins_statements_response = FinsStatementsResponse(**res.json())
    fins_statements_result = FinsStatementsResult(fins_statements_response)
    return fins_statements_result
