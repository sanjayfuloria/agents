# Creating Multiple Agents - Quick Start

This directory contains a comprehensive guide and practical examples for creating multiple agents across different AI frameworks.

## 📚 Main Guide
**[13_creating_multiple_agents.ipynb](13_creating_multiple_agents.ipynb)** - Complete guide covering:
- Multi-agent patterns (Sequential, Parallel, Hierarchical, Peer-to-Peer) 
- Examples for AutoGen, CrewAI, LangGraph, and OpenAI Agents SDK
- Best practices and framework comparisons
- Real-world use cases

## 🚀 Practical Examples
**[multi_agent_examples.py](multi_agent_examples.py)** - Runnable Python script with examples:

```bash
# Agent factory pattern (no API key needed)
python multi_agent_examples.py --example factory

# AutoGen sequential workflow (requires OpenAI API key)
python multi_agent_examples.py --example autogen_sequential

# AutoGen group chat (requires OpenAI API key)  
python multi_agent_examples.py --example autogen_group

# LangGraph multi-agent workflow (requires OpenAI API key)
python multi_agent_examples.py --example langgraph_multi
```

## 🔑 Setup
For examples requiring an API key, create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

## 🎯 Quick Start
1. Read the main guide: `13_creating_multiple_agents.ipynb`
2. Run the factory example: `python multi_agent_examples.py --example factory`
3. Try a framework-specific example with your API key
4. Explore existing examples in the framework directories:
   - `5_autogen/world.py` - Dynamic agent creation
   - `3_crew/debate/` - CrewAI team collaboration  
   - `4_langgraph/sidekick.py` - LangGraph patterns

## 🔗 Framework Examples
- **AutoGen**: `../5_autogen/` - Dynamic conversations and distributed agents
- **CrewAI**: `../3_crew/` - Structured team workflows  
- **LangGraph**: `../4_langgraph/` - Graph-based orchestration
- **OpenAI SDK**: `../2_openai/` - Production-ready workflows