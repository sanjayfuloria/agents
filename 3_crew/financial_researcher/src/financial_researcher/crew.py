# src/financial_researcher/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .tools.financial_tools import FinancialDataTool, SECFilingTool, MarketSentimentTool

@CrewBase
class ResearchCrew():
    """Comprehensive financial research crew for in-depth company analysis"""

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[SerperDevTool(), ScrapeWebsiteTool()]
        )

    @agent
    def quantitative_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['quantitative_analyst'],
            verbose=True,
            tools=[FinancialDataTool(), SECFilingTool()]
        )

    @agent
    def sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_analyst'],
            verbose=True,
            tools=[SerperDevTool(), MarketSentimentTool()]
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def quantitative_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['quantitative_analysis_task']
        )

    @task
    def sentiment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['sentiment_analysis_task']
        )

    @task
    def comprehensive_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['comprehensive_analysis_task'],
            output_file='output/comprehensive_financial_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the comprehensive financial research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )