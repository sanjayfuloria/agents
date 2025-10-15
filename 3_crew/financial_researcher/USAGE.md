# Financial Research Assistant - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
1. Python 3.10+ installed
2. CrewAI installed (`pip install 'crewai[tools]'`)
3. API keys configured (see Setup section)

### Setup
1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key  # Optional, for web search
```

2. Install dependencies:
```bash
crewai install
```

## 🔍 Running Analysis

### Basic Usage
```bash
# Run analysis on default company (Apple)
crewai run

# Or navigate to the project directory
cd src/financial_researcher
python main.py
```

### Analyze Specific Company
```bash
cd src/financial_researcher
python main.py "Tesla"  # Replace with any company name
```

### Demo Mode (No API keys required)
```bash
python demo.py
```

## 📊 What You Get

The system generates a comprehensive report including:

### 1. Executive Summary
- Investment thesis
- Key recommendations
- Risk assessment summary

### 2. Company Research
- Recent business developments
- Market position
- Competitive landscape
- Management team analysis

### 3. Financial Analysis
- Key financial ratios
- Performance trends
- Peer comparisons
- Valuation metrics

### 4. Market Sentiment
- News sentiment analysis
- Social media trends
- Analyst opinions
- Market catalysts

### 5. Investment Recommendations
- Buy/Hold/Sell recommendation
- Price targets (when applicable)
- Risk factors
- Investment rationale

## 🛠️ Customization

### Adding New Companies
Simply change the company name in `main.py` or pass it as an argument.

### Modifying Analysis Depth
Edit the task descriptions in `config/tasks.yaml` to focus on specific areas.

### Adding New Tools
Create new financial tools in `tools/financial_tools.py` and add them to the appropriate agents.

## 🔧 Advanced Features

### Training the Model
```bash
crewai train
```

### Testing
```bash
crewai test
```

### Replay Analysis
```bash
crewai replay
```

## 📝 Example Output Structure

```
output/comprehensive_financial_report.md
├── Executive Summary
├── Company Overview
├── Financial Performance Analysis
├── Market Position & Competition
├── Sentiment Analysis
├── SWOT Analysis
├── Investment Recommendations
└── Risk Assessment
```

## ⚠️ Important Notes

1. **Not Financial Advice**: This tool is for research and educational purposes only
2. **API Costs**: Running analysis requires API calls which may incur costs
3. **Data Quality**: Results depend on the quality of available data sources
4. **Demo Data**: Some tools use placeholder data for demonstration

## 🆘 Troubleshooting

### Common Issues
- **No API Key**: Make sure `OPENAI_API_KEY` is set in your environment
- **Import Errors**: Ensure all dependencies are installed via `crewai install`
- **Connection Issues**: Check internet connectivity for real-time data

### Getting Help
- Check the main README.md for detailed documentation
- Visit [crewAI documentation](https://docs.crewai.com)
- Join the [crewAI Discord community](https://discord.com/invite/X4JWnZnxPb)

## 🎯 Best Practices

1. **Start with Demo**: Use `python demo.py` to understand the system
2. **Check Output**: Review generated reports in the `output/` directory
3. **Monitor Costs**: Keep track of API usage and costs
4. **Validate Results**: Cross-check important findings with additional sources
5. **Regular Updates**: Keep the system updated for best performance

---

**Ready to analyze?** Run `crewai run` and let the AI agents do the research for you! 📈