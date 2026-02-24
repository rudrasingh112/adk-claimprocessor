from google.adk.agents import Agent
from .tools import calculate_payout, get_user_data, create_user


insurance_seller_agent = Agent(name="insurance_sales_agent",
                               model= "gemini-2.0-flash",
                               description="Understand the user requirement and suggest them the most sutaible insurance",
                               instruction="""
                                You are a Insurance Sales Agent for Yogesh Insurance Company, you sell car insurance.

                                1. Ask details about what sort of insurance they want to buy and gather information about their needs
                                2. Query the datastore and get the detail about that matches the user requirement.
                                3. Show the user how the following insurance matches their requirement. 
                                4. Always display the results in Markdown format.
                                """,
                                output_key="insurance_details"
                               )

claims_processing_agent = Agent(
    name="claims_processing_agent",
    model="gemini-2.0-flash",
    description="Help users file new insurance claims and calculate potential payouts.",
    instruction="""
    You are a Claims Adjuster for Yogesh Insurance Company.
    
    1. Assist the user in reporting an incident (user_id, date, type of damage, amount, car details).
    2. Use the 'calculate_payout' and 'get_user_data' tool to determine the reimbursement based on their deductible.
    3. Explain the payout breakdown clearly. 
    """,
    # Note: Ensure calculate_payout tool is passed in your root_agent or here
    output_key="claim_status",
    tools=[calculate_payout,get_user_data]
)

faq_agent = Agent(
    name="faq_agent",
    model="gemini-2.0-flash",
    description="Answer general questions about policy terms, coverage limits, and company procedures.",
    instruction="""
    You are a Knowledge Expert for Yogesh Insurance Company.
    
    1. Answer questions regarding general car insurance terminology (e.g., 'What is a deductible?').
    2. Use the 'LoadMemoryTool' to search for specific policy clauses if the user provides a policy ID.
    3. Do not process claims or suggest new insurance; stick to providing information.
    4. If you don't know the answer, refer the user to human support.
    """,
    output_key="faq_response"
)

account_creating = Agent(
    name="onboarding_agent",
    model="gemini-2.0-flash",
    description="Handles registration of new customers.",
    instruction="""
    You are an Onboarding Specialist. 
    1. Collect the following 4 pieces of information from the user: First Name, Last Name, Phone Number, and desired Plan (e.g., Gold, Silver).
    2. Once all 4 fields are gathered, call the 'create_user' tool.
    3. If successful, provide the user with their new 'user_id' and welcome them to Yogesh Insurance.
    """,
    tools=[create_user]
)