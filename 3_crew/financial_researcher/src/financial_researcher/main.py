#!/usr/bin/env python
# src/financial_researcher/main.py
import os
import sys
from financial_researcher.crew import ResearchCrew


# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)


def run():
    """
    Run the comprehensive financial research crew.
    """
    # Default company for demonstration
    default_company = 'Apple'
    
    # Allow command line input for company
    if len(sys.argv) > 1:
        company = sys.argv[1]
    else:
        company = default_company
    
    print(f"🔍 Starting comprehensive financial research for: {company}")
    print("=" * 60)
    print("This analysis will include:")
    print("• Company research and recent developments")
    print("• Quantitative financial analysis")
    print("• Market sentiment analysis") 
    print("• Comprehensive investment analysis report")
    print("=" * 60)
    
    inputs = {
        'company': company
    }

    try:
        # Create and run the crew
        result = ResearchCrew().crew().kickoff(inputs=inputs)

        # Print the result
        print("\n\n" + "=" * 60)
        print("📊 COMPREHENSIVE FINANCIAL ANALYSIS COMPLETE")
        print("=" * 60)
        print(result.raw)

        print(f"\n\n✅ Complete financial research report has been saved to:")
        print(f"   📄 output/comprehensive_financial_report.md")
        print(f"\n💡 This analysis covers:")
        print(f"   • Executive summary and investment thesis")
        print(f"   • Financial performance and ratio analysis")
        print(f"   • Market sentiment and competitive position")
        print(f"   • Risk assessment and investment recommendations")
        print(f"\n⚠️  Disclaimer: This analysis is for informational purposes only")
        print(f"   and should not be considered as financial advice.")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        print(f"💡 Make sure you have the required API keys configured in your environment.")
        print(f"   You may need OPENAI_API_KEY and SERPER_API_KEY for full functionality.")


def train():
    """
    Train the crew for better performance.
    """
    inputs = {
        'company': 'Apple'
    }
    try:
        ResearchCrew().crew().train(n_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 1, 
                                   filename=sys.argv[2] if len(sys.argv) > 2 else None, 
                                   inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResearchCrew().crew().replay(task_id=sys.argv[1] if len(sys.argv) > 1 else None)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'company': 'Apple'
    }
    try:
        ResearchCrew().crew().test(n_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 1, 
                                  openai_model_name=sys.argv[2] if len(sys.argv) > 2 else None, 
                                  inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['train', 'replay', 'test']:
        if sys.argv[1] == 'train':
            train()
        elif sys.argv[1] == 'replay':
            replay()
        elif sys.argv[1] == 'test':
            test()
    else:
        run()