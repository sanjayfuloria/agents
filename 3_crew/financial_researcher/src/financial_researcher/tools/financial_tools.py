from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import json
from datetime import datetime, timedelta


class FinancialDataInput(BaseModel):
    """Input schema for financial data tool."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, GOOGL)")
    metric: str = Field(..., description="Financial metric to retrieve (e.g., 'overview', 'earnings', 'ratios')")


class FinancialDataTool(BaseTool):
    name: str = "financial_data_tool"
    description: str = (
        "Retrieves financial data for a given stock ticker including company overview, "
        "earnings data, financial ratios, and key metrics. Useful for fundamental analysis."
    )
    args_schema: Type[BaseModel] = FinancialDataInput

    def _run(self, ticker: str, metric: str) -> str:
        """
        Retrieve financial data for a given ticker.
        Note: This is a demo implementation using free APIs.
        """
        ticker = ticker.upper().strip()
        
        try:
            if metric.lower() == 'overview':
                return self._get_company_overview(ticker)
            elif metric.lower() == 'earnings':
                return self._get_earnings_data(ticker)
            elif metric.lower() == 'ratios':
                return self._get_financial_ratios(ticker)
            else:
                return f"Available metrics: overview, earnings, ratios. You requested: {metric}"
                
        except Exception as e:
            return f"Error retrieving financial data for {ticker}: {str(e)}"

    def _get_company_overview(self, ticker: str) -> str:
        """Get company overview information."""
        # This is a placeholder implementation
        # In a real implementation, you would use APIs like Alpha Vantage, Yahoo Finance, or Polygon
        overview_data = {
            "ticker": ticker,
            "company_name": f"{ticker} Corporation",
            "sector": "Technology",
            "market_cap": "Large Cap",
            "description": f"Financial data for {ticker} - this is demo data",
            "note": "This is demonstration data. In production, connect to financial data APIs."
        }
        
        return json.dumps(overview_data, indent=2)

    def _get_earnings_data(self, ticker: str) -> str:
        """Get earnings information."""
        earnings_data = {
            "ticker": ticker,
            "latest_quarter": "Q3 2024",
            "eps": "Demo EPS data",
            "revenue": "Demo revenue data",
            "note": "This is demonstration data. In production, connect to financial data APIs."
        }
        
        return json.dumps(earnings_data, indent=2)

    def _get_financial_ratios(self, ticker: str) -> str:
        """Get financial ratios."""
        ratios_data = {
            "ticker": ticker,
            "pe_ratio": "Demo P/E ratio",
            "debt_to_equity": "Demo D/E ratio",
            "roe": "Demo ROE",
            "note": "This is demonstration data. In production, connect to financial data APIs."
        }
        
        return json.dumps(ratios_data, indent=2)


class SECFilingInput(BaseModel):
    """Input schema for SEC filing tool."""
    ticker: str = Field(..., description="Stock ticker symbol")
    filing_type: str = Field(..., description="Type of SEC filing (e.g., '10-K', '10-Q', '8-K')")


class SECFilingTool(BaseTool):
    name: str = "sec_filing_tool"
    description: str = (
        "Retrieves and analyzes SEC filings for companies including 10-K annual reports, "
        "10-Q quarterly reports, and 8-K current reports. Useful for regulatory compliance analysis."
    )
    args_schema: Type[BaseModel] = SECFilingInput

    def _run(self, ticker: str, filing_type: str) -> str:
        """
        Retrieve SEC filing information.
        Note: This is a demo implementation.
        """
        ticker = ticker.upper().strip()
        filing_type = filing_type.upper().strip()
        
        try:
            # This is a placeholder implementation
            # In production, you would use SEC EDGAR API
            filing_data = {
                "ticker": ticker,
                "filing_type": filing_type,
                "filing_date": "2024-03-15",
                "summary": f"Demo {filing_type} filing analysis for {ticker}",
                "key_points": [
                    "Revenue growth trends",
                    "Risk factors",
                    "Management discussion",
                    "Financial position"
                ],
                "note": "This is demonstration data. In production, connect to SEC EDGAR API."
            }
            
            return json.dumps(filing_data, indent=2)
            
        except Exception as e:
            return f"Error retrieving SEC filing for {ticker}: {str(e)}"


class MarketSentimentInput(BaseModel):
    """Input schema for market sentiment tool."""
    ticker: str = Field(..., description="Stock ticker symbol")
    timeframe: str = Field(..., description="Timeframe for sentiment analysis (e.g., '1d', '1w', '1m')")


class MarketSentimentTool(BaseTool):
    name: str = "market_sentiment_tool"
    description: str = (
        "Analyzes market sentiment for a given stock using news articles, social media, "
        "and analyst reports. Provides sentiment score and key sentiment drivers."
    )
    args_schema: Type[BaseModel] = MarketSentimentInput

    def _run(self, ticker: str, timeframe: str) -> str:
        """
        Analyze market sentiment for a stock.
        Note: This is a demo implementation.
        """
        ticker = ticker.upper().strip()
        
        try:
            # This is a placeholder implementation
            # In production, you would use sentiment analysis APIs
            sentiment_data = {
                "ticker": ticker,
                "timeframe": timeframe,
                "sentiment_score": "Neutral (0.1)",
                "sentiment_range": "-1.0 (Very Negative) to +1.0 (Very Positive)",
                "key_sentiment_drivers": [
                    "Earnings announcement",
                    "Industry trends",
                    "Market conditions"
                ],
                "news_volume": "Moderate",
                "social_media_mentions": "High",
                "note": "This is demonstration data. In production, integrate with sentiment analysis APIs."
            }
            
            return json.dumps(sentiment_data, indent=2)
            
        except Exception as e:
            return f"Error analyzing sentiment for {ticker}: {str(e)}"