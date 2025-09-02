#!/usr/bin/env python
"""
Setup script for the Financial Research Assistant
"""

import os
import sys

def create_env_file():
    """Create a template .env file if it doesn't exist"""
    env_path = '.env'
    
    if not os.path.exists(env_path):
        env_template = """# Financial Research Assistant API Keys
# Get your OpenAI API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Get your Serper API key from: https://serper.dev (Optional for web search)
SERPER_API_KEY=your_serper_api_key_here

# Optional: Other financial data API keys
# POLYGON_API_KEY=your_polygon_api_key_here
# ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
"""
        
        with open(env_path, 'w') as f:
            f.write(env_template)
        print(f"✅ Created {env_path} template file")
        print(f"📝 Please edit {env_path} and add your API keys")
        return False
    else:
        print(f"✅ .env file already exists")
        return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import crewai
        print(f"✅ CrewAI installed (version {crewai.__version__})")
        
        import openai
        print(f"✅ OpenAI library available")
        
        from crewai_tools import SerperDevTool
        print(f"✅ CrewAI tools available")
        
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print(f"💡 Install with: pip install 'crewai[tools]'")
        return False

def check_api_keys():
    """Check if API keys are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    serper_key = os.getenv('SERPER_API_KEY')
    
    keys_ok = True
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print(f"❌ OPENAI_API_KEY not configured")
        print(f"   Get your key from: https://platform.openai.com/api-keys")
        keys_ok = False
    else:
        print(f"✅ OPENAI_API_KEY configured")
    
    if not serper_key or serper_key == 'your_serper_api_key_here':
        print(f"⚠️  SERPER_API_KEY not configured (optional)")
        print(f"   Get your key from: https://serper.dev for web search")
    else:
        print(f"✅ SERPER_API_KEY configured")
    
    return keys_ok

def run_setup():
    """Run the complete setup process"""
    print("🔧 Financial Research Assistant Setup")
    print("=" * 40)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    print("✅ Output directory ready")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    # Create/check .env file
    print("\n🔑 Checking API configuration...")
    env_exists = create_env_file()
    
    # Check API keys if .env exists
    if env_exists:
        keys_ok = check_api_keys()
    else:
        keys_ok = False
    
    # Test system
    print("\n🧪 Testing system...")
    try:
        sys.path.append('src')
        from financial_researcher.crew import ResearchCrew
        crew = ResearchCrew()
        print(f"✅ System test passed")
        print(f"   - {len(crew.crew().agents)} agents ready")
        print(f"   - {len(crew.crew().tasks)} tasks configured")
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False
    
    # Summary
    print("\n📋 Setup Summary")
    print("=" * 20)
    
    if deps_ok and keys_ok:
        print("🎉 Setup complete! You're ready to run financial analysis.")
        print("\n🚀 Next steps:")
        print("   1. Run: crewai run")
        print("   2. Or: python demo.py")
        print("   3. Check output in: output/")
    elif deps_ok:
        print("⚠️  Setup partially complete.")
        print("   - Dependencies: ✅")
        print("   - API Keys: ❌")
        print("\n🔧 To complete setup:")
        print("   1. Edit .env file with your API keys")
        print("   2. Run this setup script again")
    else:
        print("❌ Setup incomplete.")
        print("\n🔧 To complete setup:")
        print("   1. Install dependencies: pip install 'crewai[tools]'")
        print("   2. Configure API keys in .env file")
        print("   3. Run this setup script again")
    
    return deps_ok and keys_ok

if __name__ == "__main__":
    try:
        run_setup()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("💡 Please check the README.md for manual setup instructions")