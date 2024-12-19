from groq import Groq
from api_key import API_KEY
import re

client = Groq(api_key=API_KEY)
MODEL = "llama-3.1-8b-instant"

def process_query(query, model=MODEL, temperature=0.3, max_tokens=2000):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role' : 'system',
                'content' : ' You are a highly advanced language model trained to extract key entities, identify the phase (a detailed description of the action or context related to the entity/entities).'
            },
            {
                'role':'user',
                'content': f"""
    You are a highly advanced language model trained to extract key entities, identify the phase (a detailed description of the action or context related to the entity/entities), and classify user queries into one of the following five categories:

    News updates: News about events, market fluctuations, shocking news, or positive developments related to blockchain.
    Analysis and forecasts: Posts containing analysis, predictions, and insights about blockchain trends.
    Educational content: Knowledge sharing posts, tutorials, or guides about blockchain.
    Product or service promotion: Posts introducing blockchain-related products or services.
    Interactive content: Engagement-focused posts, including Q&A, challenges, giveaways, polls, or surveys.

    Given the query, your task is to:

    Extract the main entity or entities mentioned in the query.
    Identify the phase of the entity/entities as a detailed phrase or action describing their context or purpose (e.g., “set up a smart contract on Ethereum,” “price fluctuations of Bitcoin”).
    Classify the query into one of the five categories listed above.

    Input:

    User query: {query}

    Output format:

    Main entity/entities: [list of entities]
    Entity phase: [detailed phase or action associated with each entity]
    Query classification: [category from the list above]

    Example Input:
    "Write a post updating the fluctuations in Bitcoin price."

    Example Output:

    Main entity/entities: [Bitcoin]
    Entity phase: [price fluctuations of Bitcoin]
    Query classification: News updates

    Another Example Input:
    "Teach me how to set up a smart contract on Ethereum."

    Example Output:

    Main entity/entities: [Ethereum, smart contract]
    Entity phase: [set up a smart contract on Ethereum]
    Query classification: Educational content

    Make sure the output is concise, accurate, and strictly adheres to the given format. The phase must always be a detailed phrase describing the specific action or context.
    """
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    response = chat_completion.choices[0].message.content
    # Process each line
    for line in response.split("\n"):
        if line.startswith("Main entity/entities:"):
            entities = re.findall(r"\[(.*?)\]", line)[0].split(", ")
        elif line.startswith("Entity phase:"):
             phase = re.findall(r"\[(.*?)\]", line)[0].split(", ")
        elif line.startswith("Query classification:"):
            classification = line.split(":", 1)[1].strip()
    
    return entities, phase, classification


