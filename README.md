Multi-Agent AI Chat Application (Powered by Google ADK)

This project is a multi-agent intelligent chat system developed for NuGenomics using the Google Agent Development Kit (ADK) and Flask.
It features a central Coordinator (Router) Agent that smartly routes user queries to one of two specialized agents —
a Customer Support Agent (for company-related FAQs) and a Genetic Wellness Agent (for general DNA and wellness questions).

The chatbot demonstrates real-world AI orchestration, prompt routing, and dynamic knowledge integration in a single application.

🔹 Key Features

1. Advanced Multi-Agent Architecture
A Coordinator Agent analyzes user intent and routes the query to the correct expert agent.

2. Google ADK Integration
Built entirely on Google’s Agent Development Kit (google-adk) to create, manage, and coordinate LLM agents with real-time reasoning and session control.

3. Dynamic Prompt Engineering

The Customer Support Agent loads its knowledge base dynamically from a scraped_faqs.json file containing NuGenomics FAQs.

The Coordinator Agent uses contextual examples from the FAQ data to improve routing accuracy.

4. Smart Routing Logic
The system automatically detects whether a query relates to NuGenomics services or general genetics and wellness and then selects the right sub-agent.

5. Flask-Powered Web Interface
A clean chat UI built using HTML, CSS, and JavaScript connects to the Flask backend through REST APIs for smooth, real-time communication.

6. Transparent Responses
Each response clearly displays which agent (Coordinator, NuGenomics, or Wellness) handled the query.

🔹 Project Architecture
my_agent/
│── __init__.py                
│── agent.py                    
│── customer_service_agent.py   
│── genetic_wellness_agent.py   
│── instruction.py             

templates/
│── index.html                 

server.py                     
scraped_faqs.json         
requirements.txt             

🔹 My Role and Development Process
🧩 System Design

I designed the overall multi-agent architecture — defining the purpose and relationship of each agent (Coordinator, Customer Support, and Wellness).

🧠 Agent Implementation

I implemented each agent using LlmAgent from the Google ADK and connected them using AgentTool for delegation and coordination.

⚙️ Prompt Engineering

Each agent has a dedicated instruction prompt to ensure correct behavior.

The Coordinator handles routing logic.

The Customer Support Agent relies on scraped FAQ data.

The Wellness Agent handles general queries using Gemini’s foundational knowledge.

🔄 Integration & Debugging

Integrated ADK components like Runner, SessionService, and async workflows with Flask.
Debugged asynchronous communication to ensure real-time response streaming.

🔹 How I Leveraged AI Assistance

ChatGPT (OpenAI GPT-5) – Used for refining code structure, debugging async event handling, and improving agent routing logic.
GitHub Copilot – Helped in generating Flask boilerplate and quick code completion.
Perplexity & Gemini – Used as research tools for resolving API integration and model configuration doubts.

AI tools acted as coding assistants and technical advisors throughout the project while all integration and testing were done manually by me.

🔹 Setup and Installation

Clone the Repository

git clone <your-repository-link>
cd <your-repository-folder>


Create and Activate Virtual Environment

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Install Dependencies

pip install -r requirements.txt


Set Google API Key
Create a .env file in your root directory:

GOOGLE_API_KEY="YOUR_API_KEY_HERE"


Run the Application

python server.py


Open the Chatbot
Visit:

http://127.0.0.1:5000

🔹 Example Test Cases

"What are the NuGenomics DNA test services?" → Customer Support Agent

"How long does it take to get my report?" → Customer Support Agent

"What is DNA methylation?" → Genetic Wellness Agent

"How does exercise affect genetics?" → Genetic Wellness Agent

"How can I contact NuGenomics?" → Customer Support Agent

🔹 Requirements

flask
flask_cors
python-dotenv
google-adk
google-generativeai
colorama
aiohttp

🔹 Developer Details

Name: Mebin Sam
Course: B.Tech in Computer Science
College: Vidya Academy of Science and Technology
Email: mebinsam7@gmail.com

🔹 Summary

The NuGenomics Multi-Agent Chatbot demonstrates how multiple AI agents can work together to handle distinct domains of knowledge within a single application.
It showcases intelligent query routing, dynamic prompt integration, and seamless communication between multiple specialized agents — all built using Google’s ADK and Flask.# AI_Chatbot_genetics
An intelligent multi-agent chatbot built using the Google Agent Development Kit (ADK) and Gemini 2.5 Flash, designed to handle both customer support and genetic wellness queries.
