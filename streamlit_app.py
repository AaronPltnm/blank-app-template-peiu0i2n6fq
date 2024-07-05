from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool

class DisasterReliefAgents:

    def __init__(self):
        self.serper = SerperDevTool()
        self.web = WebsiteSearchTool()
        self.web_scrape = ScrapeWebsiteTool()

        self.gpt4 = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.7)
        
        self.llama3_8b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get("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"), model_name="llama3-8b-8192")
        
        self.selected_llm = self.gpt4

    def data_collector(self):
        return Agent(
            role='Data Collector',
            goal='Gather data from various sources about the earthquake and its aftermath.',
            backstory="You are an expert in collecting and validating data from multiple sources.",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
            tools=[self.serper, self.web, self.web_scrape],
        )

    def data_analyst(self):
        return Agent(
            role='Data Analyst',
            goal='Analyze the collected data to identify key areas needing immediate attention.',
            backstory="You are skilled in analyzing complex data to find actionable insights.",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
        )

    def decision_maker(self):
        return Agent(
            role='Decision Maker',
            goal='Use the analyzed data to make informed decisions on resource allocation.',
            backstory="You excel at making strategic decisions based on data insights.",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
        )

class DisasterReliefTasks:

    def data_collection_task(self, agent, inputs):
        return Task(
            agent=agent,
            description=f"Collect data from various sources about the earthquake and its aftermath. Inputs: {inputs}",
            expected_output="A comprehensive report on the collected data."
        )

    def data_analysis_task(self, agent, context):
        return Task(
            agent=agent,
            context=context,
            description="Analyze the collected data to identify key areas needing immediate attention.",
            expected_output="An analysis report highlighting critical areas and needs."
        )

    def decision_making_task(self, agent, context, inputs):
        return Task(
            agent=agent,
            context=context,
            description=f"Based on the analysis report, make informed decisions on resource allocation. Inputs: {inputs}",
            expected_output="A strategic plan for resource allocation and relief efforts."
        )

class DisasterReliefCrew:
    
    def __init__(self, inputs):
        self.inputs = inputs
        self.agents = DisasterReliefAgents()
        self.tasks = DisasterReliefTasks()

    def run(self):
        data_collector = self.agents.data_collector()
        data_analyst = self.agents.data_analyst()
        decision_maker = self.agents.decision_maker()

        data_collection_task = self.tasks.data_collection_task(data_collector, self.inputs)
        data_analysis_task = self.tasks.data_analysis_task(data_analyst, [data_collection_task])
        decision_making_task = self.tasks.decision_making_task(decision_maker, [data_analysis_task], self.inputs)

        crew = Crew(
            agents=[data_collector, data_analyst, decision_maker],
            tasks=[data_collection_task, data_analysis_task, decision_making_task],
            process=Process.sequential
        )

        return crew.kickoff()

if __name__ == "__main__":
    print("Welcome to the Disaster Relief Crew Setup")
    print("---------------------------------------")
    topic = "Earthquake Disaster Relief"
    detailed_questions = input("Please enter specific aspects or areas you are focusing on for the relief efforts: ")

    inputs = f"Topic: {topic}\nDetailed Questions: {detailed_questions}"
    disaster_relief_crew = DisasterReliefCrew(inputs)
    result = disaster_relief_crew.run()

    print("\n\n##############################")
    print("## Here are the results of your disaster relief project:")
    print("##############################\n")
    print(result)

import streamlit as st

st.title('Disaster Relief Assistant')
os.environ["sk-proj-m8rW2nfxSRiaijrUpBDHT3BlbkFJ9CwlFI2AnRPyVjRYke1r"] = st.secrets["sk-proj-m8rW2nfxSRiaijrUpBDHT3BlbkFJ9CwlFI2AnRPyVjRYke1r"]
os.environ["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"] = st.secrets["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"]
os.environ["9363dd83374fd4a2dc5fb7bbe6f1d1046c4fd4bf"] = st.secrets["9363dd83374fd4a2dc5fb7bbe6f1d1046c4fd4bf"]

with st.sidebar:
    st.header('Enter Relief Details')
    detailed_questions = st.text_area("Specific aspects or areas you are focusing on for the relief efforts:")

if st.button('Run Relief Operations'):
    if not detailed_questions:
        st.error("Please fill all the fields.")
    else:
        inputs = f"Disaster Relief Topic: Earthquake Disaster Relief\nDetailed Questions: {detailed_questions}"
        disaster_relief_crew = DisasterReliefCrew(inputs)
        result = disaster_relief_crew.run()
        st.subheader("Results of your disaster relief project:")
        st.write(result)
