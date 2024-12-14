from groq import Groq
from api_key import API_KEY

client = Groq(api_key=API_KEY)
MODEL = "llama-3.3-70b-versatile"

def extract_paragraphs(text, model=MODEL, temperature=0.3, max_tokens=2000):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an advanced natural language processing tool."
            },
            {
                "role": "user",
                "content": (
                    "Your task is to extract, structure, and summarize paragraphs from a crawled web post. "
                    "The extracted paragraphs must strictly focus on **one of the following blockchain-related themes** and include relevant **statistics**:\n"
                    "1. **Analysis of the blockchain topic**: Provide insights, trends, or key observations, and ensure the paragraphs include relevant statistics.\n"
                    "2. **Future predictions or opportunities**: Highlight predictions, opportunities, or future outlooks in the blockchain industry, supported by data or statistics.\n"
                    "3. **Expert insights or actionable suggestions**: Extract professional advice, actionable tips, or insights with supporting figures, facts, or trends.\n\n"
                    "### Output Format:\n\n"
                    "'<Paragraph 1> | <Paragraph 2> | ... | <Paragraph n>' *** 'Publication date' *** 'Keyword'>\n\n"
                    "The output must be follow the above format, with each paragraph separated by a pipe (|) symbol.\n"
                    "### Instructions:\n"
                    "1. **Content**:\n"
                    "- Extract **only** paragraphs that align with one of the above themes (**Analysis**, **Future Predictions**, or **Expert Insights**).\n"
                    "- Each paragraph **must include statistics, numerical data, or measurable facts** to support the content.\n"
                    "- Ensure the paragraphs are clear, concise, and informative.\n\n"
                    "2. **Date**:\n"
                    "- Extract the publication date of the web post.\n"
                    "- Format the date as DD/MM/YYYY (e.g., 01/02/2024).\n\n"
                    "3. **Keyword**:\n"
                    "- Identify the primary entity or focus of the post, such as:\n"
                    "  - Cryptocurrencies: Bitcoin, Ethereum, Solana\n"
                    "  - Technologies: Layer-2 solutions, Lightning Network\n"
                    "  - Companies: Binance, BlackRock, Coinbase\n"
                    "  - Individuals: Elon Musk, Vitalik Buterin\n"
                    "### Key Rules:\n"
                    "- The extracted paragraphs must **strictly align with one of the three specified themes**.\n"
                    "- Ensure the content includes **relevant statistics, numerical data, or facts**.\n"
                    "- Remove irrelevant sections, such as:\n"
                    "  - Advertisements\n"
                    "  - Subscription notices\n"
                    "  - Pop-ups\n"
                    "  - Navigation links\n"
                    "  - Metadata unrelated to the core topic.\n"
                    "- Ensure all content follows the specified output format.\n"
                    "- Choose the most relevant entity as the keyword.\n\n"
                    "Now, process the following input data and provide the output in the specified format:\n"
                    f"{text}"
                )
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    
    response = chat_completion.choices[0].message.content
    content, date, keyword = "", "", ""

    try:
        content, date, keyword = response.split("***")
        content = content.split("|")
    except:
        pass
    return content, date.strip(), keyword.strip()

