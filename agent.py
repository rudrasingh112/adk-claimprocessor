import os
import uuid
import vertexai
import asyncio
from dotenv import load_dotenv
from google.adk import agents,  runners
from google.adk.sessions import VertexAiSessionService, Session
from vertexai import agent_engines 
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.runners import Runner
from google.adk.memory import VertexAiMemoryBankService
from google.genai.types import Part, Content
from google.adk.tools.load_memory_tool import LoadMemoryTool 



load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
bucket = os.getenv("GOOGLE_CLOUD_BUCKET")
app_name="claims_processor"
session_id="ses112"
user_id = 'rud'
agent_engine_id = "projects/736907218290/locations/us-central1/reasoningEngines/412394595888083763"

# --- 1. TOOLS ---
def calculate_payout(claim_amount: float, deductible: float) -> float:
    """Calculates the final insurance payout after the deductible."""
    return max(0, claim_amount - deductible)

# --- 2. AGENT DEFINITION ---
# This is the "Brain" of your project
root_agent = agents.Agent(
    name="claims_processor",
    model="gemini-2.0-flash",
    instruction="""
    You are a professional Insurance Claims Agent. 
    1. Use 'calculate_payout' tool to determine money owed to users.
    2. Use 'LoadMemoryTool' to look up previous user claims or deductible history.
    3. Be polite and professional.
    """,
    tools=[calculate_payout, LoadMemoryTool()]
)

# --- 3. SESSION & RUNNER ---
# VertexAIInMemorySessionService stores sessions in the cloud's memory


# The 'agent' variable MUST be exported for the Agent Engine to find it

# Configure Context caching

app_config = App(
    name = "claims_processor",
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
                             memory_service_builder=get_memory_service)

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
