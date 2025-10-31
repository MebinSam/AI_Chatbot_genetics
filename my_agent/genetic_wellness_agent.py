from google.adk.agents import LlmAgent

geneticwellnessagent = LlmAgent(
    model='gemini-2.5-flash', 
    name='GeneticWellnessAgent',
    description='A specialized expert for answering general queries about genetic wellness, DNA, and personalized health based on foundational knowledge.',
    instruction=(
        "You are a knowledgeable and general expert on **Genetic Wellness**. "
        "Answer questions accurately using your vast, general knowledge base. "
        "Your focus is on educational and foundational topics related to genetics and personalized health."
    ),
    # it uses foundational LLM knowledge so no tools needed
    tools=[] 
)