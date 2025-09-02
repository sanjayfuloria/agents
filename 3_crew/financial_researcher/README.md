# FinancialResearcher Crew

Welcome to the FinancialResearcher Crew project, powered by [crewAI](https://crewai.com). This advanced multi-agent AI system is designed to provide comprehensive financial research and analysis for any publicly traded company. The system leverages multiple specialized AI agents working together to deliver institutional-quality financial research reports.

## 🚀 Features

### Multi-Agent Architecture
- **Financial Researcher**: Gathers company information, recent news, and market developments
- **Quantitative Analyst**: Performs detailed financial data analysis, ratio calculations, and peer comparisons
- **Sentiment Analyst**: Analyzes market sentiment, news impact, and social media trends
- **Investment Analyst**: Synthesizes all findings into comprehensive investment analysis reports

### Advanced Analysis Capabilities
- 📊 **Financial Data Analysis**: Comprehensive ratio analysis, trend identification, and peer comparison
- 📰 **News & Market Research**: Real-time news gathering and market development tracking
- 💹 **Sentiment Analysis**: Market sentiment evaluation from multiple sources
- 📋 **SEC Filing Analysis**: Regulatory filing review and compliance analysis
- 📈 **Investment Recommendations**: Professional-grade investment thesis and risk assessment

### Comprehensive Reporting
- Executive summary with key investment thesis
- Detailed financial performance analysis
- Market position and competitive landscape assessment
- SWOT analysis and risk evaluation
- Investment recommendations with clear rationale

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Required API Keys

**Add your API keys to the `.env` file in the project root:**

```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # For web search functionality
```

## 🎯 Running the Financial Research

### Basic Usage

To analyze a company (default: Apple):
```bash
crewai run
```

### Analyze a Specific Company

To analyze a specific company, you can modify the `main.py` file or run:
```bash
cd src/financial_researcher && python main.py "Tesla"
```

### Example Companies to Analyze
- Apple (AAPL)
- Microsoft (MSFT) 
- Tesla (TSLA)
- Google/Alphabet (GOOGL)
- Amazon (AMZN)

## 📋 Analysis Output

The system generates a comprehensive financial research report that includes:

1. **Executive Summary** - Key investment thesis and recommendations
2. **Company Overview** - Business model and recent developments  
3. **Financial Analysis** - Quantitative metrics, ratios, and trends
4. **Market Position** - Competitive landscape and industry analysis
5. **Sentiment Analysis** - Market perception and news sentiment
6. **Risk Assessment** - Key risk factors and mitigation strategies
7. **Investment Recommendation** - Clear buy/hold/sell recommendation with rationale

The final report is saved as: `output/comprehensive_financial_report.md`

## 🛠 Advanced Configuration

### Customizing Agents
- Modify `src/financial_researcher/config/agents.yaml` to adjust agent roles and capabilities
- Each agent has specialized tools and expertise areas

### Customizing Analysis Tasks  
- Modify `src/financial_researcher/config/tasks.yaml` to adjust analysis depth and focus areas
- Tasks are designed to work sequentially, building upon previous analysis

### Adding Custom Tools
- Add new financial analysis tools in `src/financial_researcher/tools/`
- The system includes ready-to-use tools for financial data, SEC filings, and sentiment analysis

## 🔧 Training and Testing

Train the crew for better performance:
```bash
crewai train
```

Test the crew functionality:
```bash  
crewai test
```

Replay previous analysis:
```bash
crewai replay
```

## 📊 Sample Analysis Features

### Financial Metrics Analyzed
- Profitability ratios (ROE, ROA, Profit Margins)
- Liquidity ratios (Current Ratio, Quick Ratio)
- Leverage ratios (Debt-to-Equity, Interest Coverage)
- Efficiency ratios (Asset Turnover, Inventory Turnover)
- Valuation ratios (P/E, P/B, EV/EBITDA)

### Market Analysis
- Recent news impact assessment
- Competitive positioning analysis
- Industry trend evaluation
- Market sentiment scoring
- Social media sentiment tracking

## ⚠️ Important Disclaimers

- This system is designed for **informational and educational purposes only**
- The analysis and recommendations generated should **NOT be considered as financial advice**
- Always consult with qualified financial professionals before making investment decisions
- Past performance does not guarantee future results
- All investments carry risk of loss

## 🆘 Support and Troubleshooting

For support, questions, or feedback regarding the FinancialResearcher Crew:
- Visit the [crewAI documentation](https://docs.crewai.com)
- Check the [GitHub repository](https://github.com/joaomdmoura/crewai)
- Join the [Discord community](https://discord.com/invite/X4JWnZnxPb)

### Common Issues
- Make sure all required API keys are properly configured
- Ensure you have sufficient API credits for OpenAI and Serper
- Check internet connectivity for real-time data access

Let's create powerful financial insights together with the advanced capabilities of crewAI! 🚀📈
