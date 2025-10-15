#!/usr/bin/env python
"""
Example usage of the Financial Research Assistant
This script demonstrates how to use the enhanced financial research crew
"""

import os
import sys
from src.financial_researcher.crew import ResearchCrew

def demo_financial_research():
    """
    Demonstrate the financial research assistant capabilities
    """
    print("🔬 Financial Research Assistant Demo")
    print("=" * 50)
    
    # Example companies to analyze
    demo_companies = ['Apple', 'Tesla', 'Microsoft', 'Google']
    
    print("Available demo companies:")
    for i, company in enumerate(demo_companies, 1):
        print(f"  {i}. {company}")
    
    # For demo purposes, we'll use Apple
    selected_company = 'Apple'
    
    print(f"\n🎯 Selected Company: {selected_company}")
    print("\n📋 This demo will showcase:")
    print("  ✓ Company research and recent developments")
    print("  ✓ Quantitative financial analysis") 
    print("  ✓ Market sentiment evaluation")
    print("  ✓ Comprehensive investment report generation")
    
    print(f"\n⚠️  Note: This is a demonstration using placeholder financial data.")
    print(f"   For production use, connect to real financial data APIs.")
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    inputs = {
        'company': selected_company
    }
    
    try:
        print(f"\n🚀 Starting financial research analysis...")
        
        # Initialize and run the crew
        crew = ResearchCrew().crew()
        
        print(f"👥 Crew assembled with {len(crew.agents)} specialized agents:")
        for agent in crew.agents:
            print(f"   • {agent.role}")
        
        print(f"\n📋 Executing {len(crew.tasks)} analysis tasks...")
        
        # Note: Uncomment the next line to run actual analysis
        # This requires API keys and may take several minutes
        # result = crew.kickoff(inputs=inputs)
        
        print(f"\n✅ Analysis complete! (Demo mode - no actual API calls made)")
        print(f"📄 Report would be saved to: output/comprehensive_financial_report.md")
        
        print(f"\n📊 Expected report sections:")
        sections = [
            "Executive Summary",
            "Company Overview", 
            "Financial Performance Analysis",
            "Market Position Assessment",
            "Sentiment Analysis",
            "SWOT Analysis",
            "Investment Recommendations",
            "Risk Assessment"
        ]
        
        for section in sections:
            print(f"   📋 {section}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"💡 To run full analysis, ensure you have:")
        print(f"   • OPENAI_API_KEY in your environment")
        print(f"   • SERPER_API_KEY for web search")
        print(f"   • Internet connection for data access")

def test_tools():
    """Test the financial tools individually"""
    print("\n🛠️  Testing Financial Analysis Tools")
    print("=" * 40)
    
    try:
        from src.financial_researcher.tools.financial_tools import (
            FinancialDataTool, SECFilingTool, MarketSentimentTool
        )
        
        # Test Financial Data Tool
        print("📊 Testing Financial Data Tool...")
        fd_tool = FinancialDataTool()
        result = fd_tool._run("AAPL", "overview")
        print("✅ Financial Data Tool working")
        
        # Test SEC Filing Tool  
        print("\n📋 Testing SEC Filing Tool...")
        sec_tool = SECFilingTool()
        result = sec_tool._run("AAPL", "10-K")
        print("✅ SEC Filing Tool working")
        
        # Test Market Sentiment Tool
        print("\n💹 Testing Market Sentiment Tool...")
        sentiment_tool = MarketSentimentTool()
        result = sentiment_tool._run("AAPL", "1w")
        print("✅ Market Sentiment Tool working")
        
        print(f"\n🎉 All financial tools are operational!")
        
    except Exception as e:
        print(f"❌ Tool test error: {str(e)}")

if __name__ == "__main__":
    print("🏦 Welcome to the Financial Research Assistant")
    print("Powered by CrewAI Multi-Agent System")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test-tools':
        test_tools()
    else:
        demo_financial_research()
    
    print(f"\n📖 For full documentation, see README.md")
    print(f"🔧 To run with real data, configure API keys and use: crewai run")