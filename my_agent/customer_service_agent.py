import requests
from bs4 import BeautifulSoup
from google.adk.agents import LlmAgent 
from google.adk.tools import FunctionTool 
import json 
TARGET_URLS = [
    "https://www.nugenomics.in/faqs/","https://www.nugenomics.in/faqs/","https://www.nugenomics.in/get-in-touch","https://www.nugenomics.in/our-offerings/" 
]
def get_faq_content() -> str:

    all_content = []
    
    for url in TARGET_URLS:
        try:
            #To Fetch the content
            response = requests.get(url, timeout=15)
            response.raise_for_status() 
            
            #Inorder to Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Aggressively remove noise
            for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav', 'form']):
                script_or_style.decompose()

            # helps in identifying the source
            content = soup.get_text(separator=' ', strip=True)
            
            # Store the content with its source URL
            all_content.append({"source_url": url, "text": content})
            
        except requests.exceptions.RequestException as e:
            all_content.append({"source_url": url, "error": f"Could not fetch: {str(e)}"})
        except Exception as e:
            all_content.append({"source_url": url, "error": f"An unexpected error occurred: {str(e)}"})

    return json.dumps(all_content)
# agent used for customer service of nugenomics
customerServiceAgent = LlmAgent(
    model='gemini-2.5-flash', 
    name='NuGenomics_Query_Expert',

    instruction=(
        "You are a professional and dedicated Customer Service Agent for NuGenomics. "
        "Your ABSOLUTELY ONLY source of information for direct answers is the content you retrieve using the 'get_faq_content' tool. "
        "**CRITICAL:** You must call the 'get_faq_content' tool on the FIRST turn of every conversation. "
        "If a customer asks a general question like 'I need to know more' or 'where can I find blogs?', "
        "provide the following helpful links, but do NOT call the tool for these requests: "
        "\n\n"
        "**For in-depth articles and company updates, visit our Blog:** `https://www.nugenomics.in/knowledge-hub/` \n"
        "**For visual guides and educational content, check our Resources page:** `https://www.nugenomics.in/` \n"
        # ------------------------------------------

        "Do not answer based on general knowledge. If the answer is not in the FAQ content, state, 'I apologize, but that specific detail is not available in the company FAQs.'"
    ),
    
    tools=[
        FunctionTool(get_faq_content) 
    ]
)
