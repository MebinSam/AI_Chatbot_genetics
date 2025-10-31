import os
import traceback
import asyncio
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from colorama import Fore, Style

# Google ADK imports
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import your actual router agent
from my_agent.agent import router_agent as root_agent
load_dotenv()

APP_NAME = "NuGenomicsAgentSystem"
USER_ID = "web_user"
SESSION_ID = "session_001"

# Create runner and also store memory
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, session_service=session_service, app_name=APP_NAME)

app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_query = data.get("message", "").strip() or data.get("query", "").strip()
        if not user_query:
            return jsonify({"response": "Please enter a question."}), 400

        print(f"\n📨 User Query: {user_query}")


        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_agent_query(user_query))
        loop.close()

        
        if isinstance(result, dict):
            response_text = result.get("response", "⚠️ No response from agent.")
            source_agent = result.get("source", "Unknown Agent")
        else:
            response_text = str(result)
            source_agent = "Unknown Agent"

        print(f"🤖 Response Source: {source_agent}")
        print(f"✅ Final Answer Sent to User ({len(response_text)} chars)\n")

        return jsonify({"response": response_text, "source": source_agent})

    except Exception as e:
        print(f"❌ Server error: {type(e).__name__}: {e}")
        traceback.print_exc()
        return jsonify({"response": f"Error: {str(e)}"}), 500


async def run_agent_query(query: str) -> dict:
    """Executes the router agent and returns both text and the actual responding sub-agent name."""
    full_response = ""
    source_agent = "Unknown"

    try:
        try:
            await session_service.delete_session(
                app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
            )
        except Exception:
            pass

        await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(Fore.CYAN + f"✅ Session created: {SESSION_ID}" + Style.RESET_ALL)

        user_content = types.Content(role="user", parts=[types.Part(text=query)])
        print(Fore.YELLOW + "🚀 Running router agent (via Runner.run_async)..." + Style.RESET_ALL)

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_content
        ):
            try:
                if hasattr(event, "source"):
                    src = event.source

                    if hasattr(src, "tool_call") and hasattr(src.tool_call, "tool_name"):
                        source_agent = src.tool_call.tool_name

                    elif hasattr(src, "agent_info") and hasattr(src.agent_info, "name"):
                        source_agent = src.agent_info.name

                    elif hasattr(event, "metadata") and event.metadata:
                        source_agent = (
                            event.metadata.get("agent_name")
                            or event.metadata.get("tool_name")
                            or source_agent
                        )

            except Exception:
                pass

            if event.content and hasattr(event.content, "parts"):
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        full_response += part.text
                        print(Fore.LIGHTBLACK_EX + f"🧩 Chunk: {part.text[:70]}..." + Style.RESET_ALL)

            if hasattr(event, "is_final_response") and event.is_final_response():
                break

        readable_source = "Coordinator (Router Agent)"
        if source_agent:
            lower = source_agent.lower()
            if "customer" in lower:
                readable_source = "Customer Service Agent"
            elif "wellness" in lower:
                readable_source = "Genetic Wellness Agent"
            elif "coordinator" in lower or "router" in lower:
                readable_source = "Coordinator (Router Agent)"

        print(Fore.GREEN + f"🤖 Response Source: {readable_source}" + Style.RESET_ALL)

        if not full_response.strip():
            return {"response": "⚠️ No response from agent.", "source": readable_source}

        print(Fore.CYAN + f"✅ Final Answer Sent to User ({len(full_response)} chars)\n" + Style.RESET_ALL)
        return {"response": full_response.strip(), "source": readable_source}

    except Exception as e:
        print(Fore.RED + f"❌ Async error: {type(e).__name__}: {e}" + Style.RESET_ALL)
        traceback.print_exc()
        return {"response": f"Error: {str(e)}", "source": "Error Handler"}

if __name__ == "__main__":
    print("\n🚀 Multi-Agent routing Server Started")
    print("📍 Visit http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
