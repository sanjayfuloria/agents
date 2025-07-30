#!/usr/bin/env python3
"""
Multi-Agent Examples - Practical demonstrations of creating multiple agents

This script provides runnable examples for creating multiple agents across
different frameworks. Set your OpenAI API key in a .env file to run.

Usage:
    python multi_agent_examples.py --example autogen_sequential
    python multi_agent_examples.py --example autogen_group
    python multi_agent_examples.py --example langgraph_multi
"""

import asyncio
import argparse
from typing import List, Any, Dict
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

def check_api_key():
    """Check if OpenAI API key is available"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_key_here")
        return False
    return True

# AutoGen Examples
async def autogen_sequential_example():
    """Demonstrates sequential multi-agent workflow with AutoGen"""
    print("🤖 AutoGen Sequential Multi-Agent Example")
    print("=" * 50)
    
    try:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from autogen_agentchat.messages import TextMessage
        
        # Create model client
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        
        # Create specialized agents
        researcher = AssistantAgent(
            name="researcher",
            model_client=model_client,
            system_message="You are a research specialist. Provide concise, factual information about the given topic."
        )
        
        writer = AssistantAgent(
            name="writer", 
            model_client=model_client,
            system_message="You are a content writer. Create a brief, engaging paragraph based on research provided."
        )
        
        editor = AssistantAgent(
            name="editor",
            model_client=model_client,
            system_message="You are an editor. Review and improve the content for clarity and flow. Provide the final version."
        )
        
        print("✅ Created 3 agents: researcher, writer, editor")
        
        # Sequential workflow
        topic = "Benefits of renewable energy"
        print(f"📝 Topic: {topic}")
        print("\n🔍 Step 1: Research Phase")
        
        research_message = TextMessage(content=f"Please research: {topic}", source="user")
        research_result = await researcher.on_messages([research_message])
        research_content = research_result.chat_message.content
        print(f"Research: {research_content[:100]}...")
        
        print("\n✍️ Step 2: Writing Phase")
        write_message = TextMessage(
            content=f"Write a brief article based on this research: {research_content}", 
            source="user"
        )
        write_result = await writer.on_messages([write_message])
        article_content = write_result.chat_message.content
        print(f"Article: {article_content[:100]}...")
        
        print("\n✏️ Step 3: Editing Phase")
        edit_message = TextMessage(
            content=f"Edit and improve this article: {article_content}", 
            source="user"
        )
        final_result = await editor.on_messages([edit_message])
        final_content = final_result.chat_message.content
        
        print("\n🎉 Final Result:")
        print("-" * 40)
        print(final_content)
        print("-" * 40)
        
    except ImportError as e:
        print(f"❌ Error importing AutoGen: {e}")
        print("Make sure autogen-agentchat is installed: pip install autogen-agentchat")
    except Exception as e:
        print(f"❌ Error running AutoGen example: {e}")

async def autogen_group_chat_example():
    """Demonstrates group chat multi-agent collaboration with AutoGen"""
    print("🤖 AutoGen Group Chat Multi-Agent Example")
    print("=" * 50)
    
    try:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from autogen_agentchat.teams import RoundRobinGroupChat
        from autogen_agentchat.messages import TextMessage
        
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        
        # Create diverse agents
        analyst = AssistantAgent(
            name="analyst",
            model_client=model_client,
            system_message="You are a business analyst. Provide data-driven insights and analysis."
        )
        
        creative = AssistantAgent(
            name="creative",
            model_client=model_client,
            system_message="You are a creative thinker. Provide innovative ideas and creative solutions."
        )
        
        critic = AssistantAgent(
            name="critic",
            model_client=model_client,
            system_message="You are a constructive critic. Point out potential issues and suggest improvements."
        )
        
        print("✅ Created 3 agents: analyst, creative, critic")
        
        # Create group chat
        team_chat = RoundRobinGroupChat([analyst, creative, critic])
        
        topic = "Starting a small tech business"
        print(f"📝 Topic: {topic}")
        print("\n💬 Group Discussion:")
        
        message = TextMessage(
            content=f"Let's discuss: {topic}. Each agent should contribute their perspective in one paragraph.",
            source="user"
        )
        
        result = await team_chat.run(task=message)
        
        print("\n🎉 Group Discussion Result:")
        print("-" * 40)
        print(result.messages[-1].content if result.messages else "No result generated")
        print("-" * 40)
        
    except ImportError as e:
        print(f"❌ Error importing AutoGen: {e}")
    except Exception as e:
        print(f"❌ Error running AutoGen group chat example: {e}")

# LangGraph Example
async def langgraph_multi_agent_example():
    """Demonstrates multi-agent workflow with LangGraph"""
    print("🤖 LangGraph Multi-Agent Example")
    print("=" * 50)
    
    try:
        from typing_extensions import TypedDict
        from langgraph.graph import StateGraph, START, END
        from langgraph.graph.message import add_messages
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage
        from typing import Annotated
        
        # Define state
        class MultiAgentState(TypedDict):
            messages: Annotated[List[Any], add_messages]
            stage: str
            research_done: bool
            writing_done: bool
            
        # Agent functions
        def research_agent(state: MultiAgentState):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            system_msg = SystemMessage(content="You are a research agent. Provide brief, factual information.")
            
            user_message = state["messages"][-1] if state["messages"] else HumanMessage(content="Research needed")
            messages = [system_msg, user_message]
            response = llm.invoke(messages)
            
            return {
                "messages": [response],
                "stage": "research_complete",
                "research_done": True
            }
        
        def writing_agent(state: MultiAgentState):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
            system_msg = SystemMessage(content="You are a writing agent. Create engaging content based on the research.")
            
            # Get the research from previous messages
            research_content = ""
            for msg in state["messages"]:
                if hasattr(msg, 'content'):
                    research_content = msg.content
                    break
            
            user_message = HumanMessage(content=f"Write a brief article based on: {research_content}")
            messages = [system_msg, user_message]
            response = llm.invoke(messages)
            
            return {
                "messages": [response],
                "stage": "writing_complete", 
                "writing_done": True
            }
        
        # Router function
        def route_workflow(state: MultiAgentState):
            if not state.get("research_done", False):
                return "research"
            elif not state.get("writing_done", False):
                return "writing"
            else:
                return "END"
        
        # Build graph
        graph_builder = StateGraph(MultiAgentState)
        graph_builder.add_node("research", research_agent)
        graph_builder.add_node("writing", writing_agent)
        
        graph_builder.add_conditional_edges(
            START,
            route_workflow,
            {"research": "research", "writing": "writing", "END": END}
        )
        
        graph_builder.add_conditional_edges(
            "research",
            route_workflow,
            {"writing": "writing", "END": END}
        )
        
        graph_builder.add_edge("writing", END)
        
        # Compile graph
        multi_agent_graph = graph_builder.compile()
        
        print("✅ Built LangGraph with research and writing agents")
        
        # Run workflow
        topic = "Artificial Intelligence in education"
        print(f"📝 Topic: {topic}")
        
        initial_state = {
            "messages": [HumanMessage(content=f"Research and write about: {topic}")],
            "stage": "start",
            "research_done": False,
            "writing_done": False
        }
        
        print("\n🔄 Running multi-agent workflow...")
        result = await multi_agent_graph.ainvoke(initial_state)
        
        print("\n🎉 Final Result:")
        print("-" * 40)
        final_message = result["messages"][-1]
        print(final_message.content if hasattr(final_message, 'content') else str(final_message))
        print("-" * 40)
        
    except ImportError as e:
        print(f"❌ Error importing LangGraph: {e}")
        print("Make sure langgraph is installed: pip install langgraph langchain-openai")
    except Exception as e:
        print(f"❌ Error running LangGraph example: {e}")

# Utility function to create multiple agents of different types
def create_agent_factory():
    """Demonstrates creating multiple agents with a factory pattern"""
    print("🏭 Agent Factory Pattern Example")
    print("=" * 50)
    
    agent_templates = {
        "researcher": "You are a research specialist focused on gathering accurate information.",
        "writer": "You are a creative writer focused on engaging storytelling.",
        "analyst": "You are a data analyst focused on insights and trends.",
        "critic": "You are a constructive critic focused on improvement suggestions.",
        "planner": "You are a strategic planner focused on organizing and structuring tasks."
    }
    
    created_agents = []
    
    print("🔧 Creating agents using factory pattern:")
    for role, description in agent_templates.items():
        agent_config = {
            "name": f"{role}_agent",
            "role": role,
            "description": description,
            "capabilities": ["text_processing", "analysis"],
            "id": f"agent_{len(created_agents) + 1}"
        }
        created_agents.append(agent_config)
        print(f"  ✅ Created {role} agent: {agent_config['name']}")
    
    print(f"\n📊 Summary: Created {len(created_agents)} agents")
    print("Agent roles:", [agent["role"] for agent in created_agents])
    
    return created_agents

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Examples")
    parser.add_argument(
        "--example",
        choices=["autogen_sequential", "autogen_group", "langgraph_multi", "factory"],
        default="autogen_sequential",
        help="Which example to run"
    )
    
    args = parser.parse_args()
    
    if not check_api_key() and args.example != "factory":
        return
    
    print(f"🚀 Running {args.example} example...")
    print()
    
    if args.example == "autogen_sequential":
        asyncio.run(autogen_sequential_example())
    elif args.example == "autogen_group":
        asyncio.run(autogen_group_chat_example())
    elif args.example == "langgraph_multi":
        asyncio.run(langgraph_multi_agent_example())
    elif args.example == "factory":
        create_agent_factory()
    
    print("\n✨ Example completed!")
    print("\nNext steps:")
    print("- Try running other examples with different --example arguments")
    print("- Modify the agent roles and see how it changes the output")
    print("- Check out the comprehensive guide in guides/13_creating_multiple_agents.ipynb")

if __name__ == "__main__":
    main()