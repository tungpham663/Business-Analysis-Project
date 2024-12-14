from groq import Groq
import re
from api_key import API_KEY

client = Groq(api_key=API_KEY)
MODEL = 'llama-3.3-70b-versatile'

# extract content, date, title from crawled text
def preprocess(text, model=MODEL , temperature=0.3, max_tokens=2000):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an advanced natural language processing tool."
            },
            {
                "role": "user",
                "content": (
                    "Your task is to extract and structure the content of a crawled web post "
                    "into a clear and concise format. The structured content should include:\n\n"
                    "1. Title: The cleaned and complete title of the post, without any extra symbols or formatting artifacts.\n"
                    "2. Body: The main textual content of the post, preserving its structure (e.g., paragraphs, headings) while removing irrelevant sections such as advertisements, subscription notices, or metadata unrelated to the core content.\n"
                    "3. Date: The publication date of the post.\n\n"
                    "Output format:\n\n"
                    "'Post Title' *** 'Post Body' *** 'Publication Date'\n\n"
                    "Instructions:\n"
                    "- Keep all valid content intact and well-structured.\n"
                    "- Avoid including redundant or irrelevant text.\n"
                    "- Do not provide explanations or commentary beyond the specified output format.\n"
                    "- In particular, if there are any quotations in the text, remove the double quotes (\"), and present the text in clean format "
                    "without the quotation marks.\n\n"
                    "- The date must be in the format day/month/year, for example 01/02/2024"
                    "Now, process the following input data and provide the output in the required format:\n"
                    f"{text}"
                )
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = chat_completion.choices[0].message.content
    try:
        [title, content, date] = response.split(' *** ')
    except:
        title = ""
        content = ""
        date = ""
    return title, content, date

#extract entities and relationships from crawled content
def extract(text, model=MODEL, temperature=0.1, max_tokens=2000):
    
    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": "You are an advanced natural language processing tool."
        },
        {
            "role": "user",
            "content": (
                "Entity and Relationship Extraction Task\n"
                "### Objective\n"
                "Your task is to extract entities, their relationships, and classify relationships into short-term or long-term events.\n\n"
                "For short-term relationships, include a separate time field extracted from the article (e.g., specific dates, months, quarters). "
                "Use normalized relationship names and include the exact sentence from the article as the description.\n\n"
                "### Instructions\n"
                "**Input**\n"
                "A financial article provided in text format focused on blockchain and related financial topics.\n\n"
                "**Output**\n"
                "The output must include three structured sections:\n\n"
                "1. **Entities**: A list of entities involved in at least one valid relationship.\n"
                "2. **Relationships**: Relationships between entities with normalized relationship names, an exact sentence, and an additional time field for short-term events.\n"
                "3. **Classification**: Each relationship is labeled as short-term or long-term (without any explaination).\n\n"
                "### Extraction Requirements\n"
                "1. **Entities**\n"
                "You can only extract entities only if they are part of a valid relationship. If an entity is not a part of a valid relationship, you can not list it in entities list. You only extract entitities which are one of the following types:\n\n"
                "| Entity Type        | Examples                          |\n"
                "|--------------------|-----------------------------------|\n"
                "| Cryptocurrencies   | Bitcoin (BTC), Ethereum (ETH), Solana (SOL)         |\n"
                "| Companies          | Binance, Coinbase, BlackRock      |\n"
                "| Individuals        | Elon Musk, Vitalik Buterin        |\n"
                "| Countries          | Korea, Japan, United State of America (USA)                      |\n"
                "| Technologies       | Layer-2 solutions, Lightning Network, Stacks |\n"
                "| Market Terms       | Market cap, BTC ETFs, DeFi TVL    |\n\n"
                "The name of the entity must be the full name followed by the short name in parentheses. For example, \"Bitcoin (BTC)\".\n\n"
                "### Output Format for Entities:\n"
                "Entities:\n"
                "- Entity Name: <Full Name (Short name)>\n"
                "  Entity Type: <Entity Type>\n\n"
                "2. **Relationships**\n"
                "A valid relationship must meet the following conditions:\n\n"
                "- **Direct Interaction**: The sentence must describe an explicit or meaningful interaction between two entities.\n"
                "- **Normalized Relationship Names**: Use clear, standardized phrases for the relationship names (e.g., \"support,\" \"enhance scalability for,\" \"introduce\"). "
                "Avoid vague or generic verbs like \"was,\" \"had,\" or \"underwent.\"\n"
                "- **Short-Term Relationships**: If the event is short-term (spanning days, weeks, or months), extract and include the time data.\n"
                "- **Long-Term Relationships**: Events that span multiple years, are ongoing, or if no specific time frame is given.\n\n"
                "### Classification\n"
                "Label each relationship as short-term or long-term.\n\n"
                "### Output Format for Relationships:\n"
                "Relationships:\n"
                "- Relationship: <Normalized Relationship Name>\n"
                "  Description: \"<Exact sentence from the article>\"\n"
                "  Entities: <Entity A>, <Entity B>\n"
                "  Classification: <Short-term | Long-term>\n"
                "### Output Example\n"
                "**Input Sentence**:\n"
                "\"BlackRock announced in January 2024 that it supports Bitcoin by investing heavily in BTC ETFs. "
                "The Lightning Network has been enhancing Bitcoin’s scalability for years.\"\n\n"
                "**Expected Output**:\n"
                "Entities:\n"
                "- Entity Name: BlackRock\n"
                "  Entity Type: Company\n\n"
                "- Entity Name: Bitcoin (BTC)\n"
                "  Entity Type: Cryptocurrency\n\n"
                "- Entity Name: Lightning Network\n"
                "  Entity Type: Technology\n\n"
                "- Entity Name: BTC ETFs\n"
                "  Entity Type: Market Terms\n\n"
                "Relationships:\n"
                "- Relationship: support\n"
                "  Description: \"BlackRock announced in January 2024 that it supports Bitcoin by investing heavily in BTC ETFs.\"\n"
                "  Entities: BlackRock, Bitcoin\n"
                "  Classification: Short-term\n"
                "- Relationship: enhance scalability for\n"
                "  Description: \"The Lightning Network has been enhancing Bitcoin’s scalability for years.\"\n"
                "  Entities: Lightning Network, Bitcoin\n"
                "  Classification: Long-term\n"
                "### Key Rules\n"
                "- **Short-term Relationships**: Events with specific time data (e.g., dates, months, or quarters) are classified as short-term.\n"
                "- **Long-term Relationships**: Events spanning multiple years or described as ongoing are classified as long-term.\n"
                "- **Normalized Relationship Names**: Use consistent, meaningful phrases for relationship names (e.g., \"support,\" \"introduce,\" \"enhance scalability for\").\n"
                "- **Exact Sentence**: Include the exact sentence from the article as the description.\n"
                "- **Filter Entities**: Only include entities that are part of a valid relationship.\n"
                "- **Split Relationships**: If multiple entities share the same relationship, split them into individual pairs.\n\n"
                "### Invalid Examples\n"
                "1. **No Direct Interaction**:\n"
                "\"Both Bitcoin and Ethereum underwent significant changes.\"\n"
                "Reason: No explicit interaction between Bitcoin and Ethereum.\n\n"
                "2. **Vague Relationships**:\n"
                "\"BlackRock and Fidelity are big fans of Bitcoin.\"\n"
                "Reason: \"Being fans\" does not establish a meaningful relationship.\n\n"
                "Now, process the following input data and provide the output in the required format:\n"
                f"{text}"
                )
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = chat_completion.choices[0].message.content
    return response


def extract_entities(text):
    entity_pattern = re.compile(r"- Entity Name: (.*?)\s+Entity Type: (.*?)\n")
    matches = entity_pattern.findall(text)
    
    entities = [{"Entity Name": name.strip(), "Entity Type": etype.strip()} for name, etype in matches]
    return entities

def extract_relationships(text, time):
    # Updated regex: removed strict newline requirement at the end
    pattern = re.compile(
        r"- Relationship: (.*?)\s+"       # Captures the relationship name
        r"Description: \"(.*?)\"\s+"     # Captures the description
        r"Entities: (.*?), (.*?)\s+"     # Captures Entity 1 and Entity 2
        r"Classification: (.*?)(?:\s+|$)",     # Captures the classification  
        re.DOTALL | re.MULTILINE         
    )
    
    # Find all matches using the pattern
    matches = pattern.findall(text)
    
    # Extract and format data into a list of dictionaries
    extracted_data = []
    for match in matches:
        relationship, description, entity1, entity2, classification = match
        extracted_data.append({
            "Relationship": relationship.strip(),
            "Description": description.strip(),
            "Entity 1": entity1.strip(),
            "Entity 2": entity2.strip(),
            "Classification": classification.strip(),
            "Time": time.strip()
        })
    
    return extracted_data