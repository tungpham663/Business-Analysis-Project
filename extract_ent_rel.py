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
            "content": f"""
                Entity and Relationship Extraction Task  
                ### Objective  
                Your task is to extract entities, their relationships, and classify relationships into short-term or long-term events.  

                For short-term relationships, include a separate time field extracted from the article (e.g., specific dates, months, quarters).  
                Use normalized relationship names and include the exact sentence from the article as the description.  

                ### Instructions  
                **Input**  
                A financial article provided in text format focused on blockchain and related financial topics.  

                **Output**  
                The output must include three structured sections:  

                1. **Entities**: A list of entities involved in at least one valid relationship.  
                2. **Relationships**: Relationships between entities with normalized relationship names, an exact sentence, and an additional time field for short-term events.  
                3. **Classification**: Each relationship is labeled as short-term or long-term (without any explanation).  

                ### Extraction Requirements  
                1. **Entities**  
                You can only extract entities if they are part of a valid relationship. If an entity is not part of a valid relationship, you cannot list it in the entities list. You only extract entities which are one of the following types:  

                | Entity Type        | Examples                          |  
                |--------------------|-----------------------------------|  
                | Cryptocurrencies   | Bitcoin, Ethereum, Solana         |  
                | Companies          | Binance, Coinbase, BlackRock      |  
                | Individuals        | Elon Musk, Vitalik Buterin        |  
                | Countries          | Korea, Japan, United States       |  
                | Technologies       | Layer-2 solutions, Lightning Network, Stacks |  
                | Market Terms       | Market cap, Bitcoin ETFs, DeFi TVL    |  

                The name of the entity must always be the full name. Abbreviations, short forms, or mixed formats (e.g., BTC, Bitcoin (BTC)) are not allowed. For example, use "Bitcoin" instead of "BTC" or "Bitcoin (BTC), "Ethereum" instead of "ETH" or "Ethereum (ETH)", "Solana" instead of "Solana" or "Solana (SOL)".

                ### Output Format for Entities:  
                Entities:  
                - Entity Name: <Full Name>  
                Entity Type: <Entity Type>  

                2. **Relationships**  
                A valid relationship must meet the following conditions:  

                - **Direct Interaction**: The sentence must describe an explicit or meaningful interaction between two entities.  
                - **Normalized Relationship Names**: Use clear, standardized phrases for the relationship names (e.g., "support," "enhance scalability for," "introduce").  
                Avoid vague or generic verbs like "was," "had," or "underwent."  
                - **Short-Term Relationships**: If the event is short-term (spanning days, weeks, or months), extract and include the time data.  
                - **Long-Term Relationships**: Events that span multiple years, are ongoing, or if no specific time frame is given.  

                ### Classification  
                Label each relationship as short-term or long-term.  

                ### Output Format for Relationships:  
                Relationships:  
                - Relationship: <Normalized Relationship Name>  
                Description: "<Exact sentence from the article>"  
                Entities: <Entity A>, <Entity B>  
                Classification: <Short-term | Long-term>  

                ### Output Example  
                **Input Sentence**:  
                "BlackRock announced in January 2024 that it supports Bitcoin by investing heavily in BTC ETFs.  
                The Lightning Network has been enhancing Bitcoin’s scalability for years."  

                **Expected Output**:  
                Entities:  
                - Entity Name: BlackRock  
                Entity Type: Company  

                - Entity Name: Bitcoin  
                Entity Type: Cryptocurrency  

                - Entity Name: Lightning Network  
                Entity Type: Technology  

                - Entity Name: Bitcoin ETFs  
                Entity Type: Market Terms  

                Relationships:  
                - Relationship: support  
                Description: "BlackRock announced in January 2024 that it supports Bitcoin by investing heavily in BTC ETFs."  
                Entities: BlackRock, Bitcoin  
                Classification: Short-term  

                - Relationship: enhance scalability for  
                Description: "The Lightning Network has been enhancing Bitcoin’s scalability for years."  
                Entities: Lightning Network, Bitcoin  
                Classification: Long-term  

                ### Key Rules  
                - **Short-term Relationships**: Events with specific time data (e.g., dates, months, or quarters) are classified as short-term.  
                - **Long-term Relationships**: Events spanning multiple years or described as ongoing are classified as long-term.  
                - **Normalized Relationship Names**: Use consistent, meaningful phrases for relationship names (e.g., "support," "introduce," "enhance scalability for").  
                - **Exact Sentence**: Include the exact sentence from the article as the description.  
                - **Filter Entities**: Only include entities that are part of a valid relationship.  
                - **Split Relationships**: If multiple entities share the same relationship, split them into individual pairs.  

                ### Remove all invalid relationships:  
                1. **No Direct Interaction**:  
                "Both Bitcoin and Ethereum underwent significant changes."  
                Reason: No direct and explicit interaction between Bitcoin and Ethereum.  

                2. **Vague Relationships**:  
                "BlackRock and Fidelity are big fans of Bitcoin."  
                Reason: "Being fans" does not establish a meaningful relationship.  

                Now, process the following input data and provide the output in the required format:  
                {text}
                """
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