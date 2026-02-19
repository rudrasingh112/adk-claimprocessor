import os
import uuid
import vertexai
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.sessions import VertexAiSessionService, Session
from vertexai import agent_engines 
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.runners import Runner
from google.adk.memory import VertexAiMemoryBankService
from google.genai.types import Part, Content
from google.adk.tools.load_memory_tool import LoadMemoryTool 
from .subagents import insurance_seller_agent, faq_agent, claims_processing_agent



load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
bucket = os.getenv("GOOGLE_CLOUD_BUCKET")
app_name="claims_processor"
session_id="ses112"
user_id = 'rud'
agent_engine_id = "projects/736907218290/locations/us-central1/reasoningEngines/412394595888083763"

# --- 1. TOOLS ---


# --- 2. AGENT DEFINITION ---
# This is the "Brain" of your project
root_agent = Agent(
    name="insurance_company",
    model= "gemini-2.0-flash",
    description="Deligate the user to different sub agent on the basis of the usecase",
    instruction="""
    You are a Yogesh Insurance company chatbot.
    1. Always greet the user in a polite manner.
    2. Ask them how can you be of any help.
    3. Understant the user intent and deligate them to the different task as required.
    4. You can handle request related to buying insurance, filing a claim and faq related to claims.

    """,
    sub_agents=[insurance_seller_agent,claims_processing_agent, faq_agent]
)



# --- 3. SESSION & RUNNER ---
# VertexAIInMemorySessionService stores sessions in the cloud's memory


# The 'agent' variable MUST be exported for the Agent Engine to find it

# Configure Context caching

app_config = App(
    name = "insurance_company",
    root_agent=root_agent,
    context_cache_config= ContextCacheConfig(
        min_tokens =2048,
        ttl_seconds = 600
    ),
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,
        overlap_size = 1
        )
)

def get_session_service():
    return VertexAiSessionService(project=project_id, location=location,
                                          agent_engine_id=agent_engine_id)

def get_memory_service():
    return VertexAiMemoryBankService(project=project_id,
                                           location=location,
                                           agent_engine_id=agent_engine_id)

agent = agent_engines.AdkApp(agent = app_config,
                             session_service_builder=get_session_service,
                             memory_service_builder=get_memory_service,
                             enable_tracing=True
                             )

# async def run_scenerio():
#     runner = Runner(app= app, session_service= session_service, memory_service= memory_service)

#     await runner.session_service.create_session(app_name=app_name,
#                                                 session_id=session_id,
#                                                 user_id=user_id)
#     message = Content(parts = [Part(text="what is the reambusment amount")], role='user')
#     async for event in runner.run_async(user_id=user_id, session_id=session_id,
#                                 new_message=message):
#         if event.is_final_response() and event.content and event.content.parts:
#             final_response = event.content.parts[0].text

#     whole_session = await runner.session_service.get_session(app_name=app_name,
#                                                        user_id=user_id,
#                                                          session_id=session_id)
#     await memory_service.add_session_to_memory(whole_session)


    

    
    

    # agent = agent_engines.AdkApp(
    #         agent=root_agent,
    #         session_service_builder=session_service
    #     )
