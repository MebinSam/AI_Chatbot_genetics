from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from my_agent.customer_service_agent import customerServiceAgent
from my_agent.genetic_wellness_agent import geneticwellnessagent

#This Is The Router Agent Which routes Two Agents
router_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='CoordinatorRouterAgent',
    description='A smart routing agent that delegates queries to the correct sub-agent.',
    instruction=(
        "You are the **Coordinator Router Agent**.\n"
        "Your job is to analyze the user's query and route it to the correct expert agent using the provided tools.\n\n"

        "If the question is related to NuGenomics, reports, booking, counselling, DNA tests, or company processes, "
        "use the **customer_service_agent** tool.\n"

        "If the question is about genetics, DNA, health, or wellness, "
        "use the **genetic_wellness_agent** tool.\n\n"

        "After calling a tool, prefix your reply with one of the following exactly:\n"
        " - '🧫 NuGenomics Agent:' if it was handled by customer_service_agent\n"
        " - '🧬 Genetic Wellness Agent:' if it was handled by genetic_wellness_agent\n\n"

        "If it's just a greeting (like 'hi', 'hello', or 'thanks'), answer directly as yourself (the Coordinator).\n"
        "Otherwise, do not respond on your own — always call one of the tools."
    ),
    tools=[
        AgentTool(customerServiceAgent),
        AgentTool(geneticwellnessagent),
    ]
)

# To export
root_agent = router_agent
