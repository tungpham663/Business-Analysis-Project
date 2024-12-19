#import libraries
from groq import Groq
from api_key import API_KEY
from get_input_data import get_input_data

#API key for Groq
client = Groq(api_key=API_KEY)
MODEL = "llama-3.1-8b-instant"

#post type and their descriptions
post_types={1: "News articles announcing fluctuations, shocking news, or positive news related to blockchain (exchange/crypto, token, DeFi, NFT)",
            2: "Analytical articles, forecasts, and insights about the blockchain situation",
            3: "Blockchain knowledge-sharing articles and tutorials",
            4: "Product and service introduction articles",
            5: "Interactive articles, Q&A, Challenges, Giveaways, Polls, Surveys"}


def gen_1(keywords, paragraph="", relationships=[], model=MODEL, temperature=0.3, max_tokens=2000):
    for keyword in keywords:
        para, relations = get_input_data(keyword)
        paragraph += para
        relationships += relations
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'You are an advanced content generator specializing in creating engaging news articles related to blockchain events.'
            },
            {
                'role': 'user',
                'content': f"""
You are an advanced content generator specializing in creating engaging news articles related to blockchain events. Your task is to write a short **news post** about **fluctuations, shocking news, or positive news** in the blockchain industry, specifically in areas like crypto exchanges, tokens, DeFi, or NFTs.

---

### **Input**:
- **Keyword**: {keyword}
- **Paragraph**: {paragraph if paragraph else "None"}
- **Relationships**: 
{relationships if relationships else "None"}

---

### **Instructions**:
1. **Purpose**: The post must highlight key events, trends, or news that are shocking, exciting, or indicate positive fluctuations in the blockchain space.  
2. **Format**:
   - Start with a **headline** that is concise and attention-grabbing (e.g., "DeFi Tokens Soar Amid Pro-Crypto Policies Following Election Results").  
   - Use the keyword as the central theme of the post.  
   - Include information from the paragraph or relationships if provided. If no details are available, infer plausible and realistic blockchain-related news.  
3. **Tone**: Use a professional and engaging tone as seen in top financial or crypto news outlets like **CoinDesk**, **Bloomberg Crypto**, or **CoinTelegraph**.  
4. **Length**: The post should be around 80–150 words.  
5. **Highlight Impact**: Focus on how the event impacts tokens, DeFi, NFT, exchanges, or broader blockchain sentiment.
6. **Hastags**: Include relevant hashtags like #blockchain, #crypto, #DeFi, #NFT, #exchange, etc.
                """
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return chat_completion.choices[0].message.content

def gen_2(keywords, paragraph="", relationships=[], model=MODEL, temperature=0.3, max_tokens=2000):
    for keyword in keywords:
        para, relations = get_input_data(keyword)
        paragraph += para
        relationships += relations
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'You are an expert financial and blockchain analyst with deep knowledge of global crypto markets, trends, and technologies.'
            },
            {
                'role': 'user',
                'content': f'''
Your task is to write an **analytical article**, forecast, or insight report focusing on the blockchain industry. The article should be thought-provoking and provide valuable insights into trends, forecasts, or impacts in areas like crypto exchanges, tokens, DeFi, NFTs, or blockchain infrastructure.

---

### **Input**:
- **Keyword**: {keyword}
- **Paragraph**: {paragraph if paragraph else "None"}
- **Relationships**: 
{relationships if relationships else "None"}

---

### **Instructions**:
1. **Purpose**: Provide a detailed analysis, forecast, or insightful commentary about the blockchain industry. Focus on trends, emerging technologies, economic impacts, or critical challenges.
2. **Format**:
   - Start with a **headline** that reflects a professional and analytical tone (e.g., "Blockchain Adoption Set to Accelerate as Institutional Investments Surge").
   - Write an **introduction** that establishes the context, outlines the topic, and engages the reader.
   - Include **analysis**, supporting arguments, and expert forecasts using the keyword as the central theme.
   - Use details from the paragraph or relationships when provided. If no specific details are available, generate realistic and plausible insights.
3. **Tone**: Use a professional, insightful, and authoritative tone similar to top financial analysis reports found in **Bloomberg**, **Forbes**, or **CoinDesk Research**.
4. **Length**: The article should be 100-200 words, ensuring depth and clarity.
5. **Highlights**: Incorporate forecasts, expert insights, and impacts on key areas (e.g., DeFi, NFTs, major tokens, blockchain adoption).
6. **Conclusion**: Provide a brief forecast or outlook for the near future based on the analysis.
7. **Hastags**: Include relevant hashtags like #blockchain, #crypto, #DeFi, #NFT, #analysis, etc.
8. **Emojis**: Use emojis sparingly to emphasize key points or to maintain reader engagement.
                '''
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return chat_completion.choices[0].message.content

def gen_3(keywords, paragraph="", relationships=[], model=MODEL, temperature=0.3, max_tokens=2000):
    for keyword in keywords:
        para, relations = get_input_data(keyword)
        paragraph += para
        relationships += relations

    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'You are a knowledgeable blockchain educator and content creator, specializing in tutorials and knowledge-sharing articles for readers of all skill levels.'
            },
            {
                'role': 'user',
                'content': f'''
Your task is to write a **blockchain tutorial** or **knowledge-sharing article** that explains blockchain concepts, tools, or technologies in an engaging and easy-to-follow manner.

### **Input**:
- **Keyword**: {keyword}
- **Paragraph**: {paragraph if paragraph else "None"}
- **Relationships**: 
{relationships if relationships else "None"}

---

### **Instructions**:
1. **Purpose**: Provide a clear, detailed, and beginner-to-intermediate-level explanation or guide on the given blockchain topic. Focus on making complex topics understandable and actionable.
2. **Format**:
   - Start with a **headline** that clearly conveys the article or tutorial purpose (e.g., "A Beginner’s Guide to Smart Contracts: How They Work and Why They Matter").
   - Write an **introduction** that engages readers and explains what they will learn.
   - Include **step-by-step explanations** or **detailed insights** about the keyword topic. Use examples, analogies, or diagrams (if applicable).
   - Address any tools, technologies, or code snippets relevant to the topic.
3. **Tone**: Use a clear, educational, and approachable tone that resonates with beginners while also providing value to intermediate readers. Ensure accuracy and relevance.
4. **Length**: The tutorial or article should be 100-200 words, ensuring depth and practical value.
5. **Highlights**: Include actionable tips, real-world applications, or examples to make the topic relatable and easy to understand.
6. **Conclusion**: Summarize key takeaways and suggest next steps for readers to deepen their knowledge.
7. **Hastags**: Include relevant hashtags like #blockchain, #tutorial, #education, #smartcontracts, etc.
8. **Emojis**: Use emojis sparingly to enhance readability and engagement.
                '''
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return chat_completion.choices[0].message.content

def gen_4(keywords, paragraph="", relationships=[], model=MODEL, temperature=0.3, max_tokens=2000):
    for keyword in keywords:
        para, relations = get_input_data(keyword)
        paragraph += para
        relationships += relations
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'You are a skilled marketing content writer specializing in creating compelling product and service introduction articles for the blockchain and tech industries.'
            },
            {
                'role': 'user',
                'content': f'''
You are a skilled marketing content writer specializing in creating compelling product and service introduction articles for the blockchain and tech industries. Your task is to write an **introduction article** that highlights the features, benefits, and unique aspects of a specific product or service in the blockchain space.

---

### **Input**:
- **Keyword**: {keyword}
- **Paragraph**: {paragraph if paragraph else "None"}
- **Relationships**: 
{relationships if relationships else "None"}

---

### **Instructions**:
1. **Purpose**: Introduce a blockchain-related product or service in a clear, engaging, and persuasive manner. Focus on its key features, benefits, and unique value propositions.
2. **Format**:
   - Start with a **headline** that captures attention (e.g., "Introducing XYZ Wallet: The Secure and Seamless Way to Manage Your Crypto").
   - Write an **introduction** that briefly explains the product/service and its relevance in the market.
   - Include detailed **features** and highlight their benefits to the target audience.
   - Address **what makes the product or service unique**, such as technology, ease of use, security, or cost-effectiveness.
   - Use real-world **use cases** or examples to showcase its value.
3. **Tone**: Use a professional, engaging, and persuasive tone tailored to a tech-savvy audience.
4. **Length**: The article should be 100-200 words, providing a balance of detail and clarity.
5. **Highlights**: Emphasize the product's value, unique features, and benefits, ensuring readers understand its advantages.
6. **Conclusion**: End with a call-to-action encouraging readers to explore or adopt the product/service.
7. **Hastags**: Include relevant hashtags like #blockchain, #productlaunch, #cryptowallet, #blockchainservice, etc.
8. **Emojis**: Use emojis sparingly to enhance key points and maintain reader interest.
                '''
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return chat_completion.choices[0].message.content

def gen_5(keywords, paragraph="", relationships=[], model=MODEL, temperature=0.3, max_tokens=2000):
    for keyword in keywords:
        para, relations = get_input_data(keyword)
        paragraph += para
        relationships += relations

    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'You are a creative content strategist specializing in designing engaging interactive articles, Q&A sessions, challenges, giveaways, polls, and surveys for blockchain enthusiasts.'
            },
            {
                'role': 'user',
                'content': f'''
You are a creative content strategist specializing in designing engaging interactive articles, Q&A sessions, challenges, giveaways, polls, and surveys for blockchain enthusiasts. Your task is to write an **interactive content piece** that encourages participation and engagement from readers while centering on blockchain-related topics.

---

### **Input**:
- **Keyword**: {keyword}
- **Paragraph**: {paragraph if paragraph else "None"}
- **Relationships**: 
{relationships if relationships else "None"}

---

### **Instructions**:
1. **Purpose**: Create an engaging and interactive article or activity that involves blockchain enthusiasts. Examples include Q&A sessions, challenges, giveaways, polls, or surveys.
2. **Format**:
   - Start with a **headline** that invites readers to participate (e.g., "Take Our Blockchain Trends Survey and Win Exciting Rewards!").
   - Write an **introduction** explaining the purpose and importance of the activity.
   - Detail the interactive element: describe the Q&A, challenge, poll, or giveaway clearly with steps for participation.
   - Add a sense of urgency or incentive where applicable (e.g., "Winners will be announced next week!").
3. **Tone**: Use a fun, approachable, and engaging tone while maintaining clarity and professionalism.
4. **Length**: The content should be concise (100-200 words) but highly actionable.
5. **Highlights**: Clearly state the steps or rules for participation and emphasize benefits to the audience (e.g., rewards, knowledge sharing).
6. **Conclusion**: End with a call-to-action encouraging readers to participate.
7. **Hastags**: Include relevant hashtags like #blockchain, #crypto, #interactive, #challenge, #survey, etc.
8. **Emojis**: Use emojis to enhance the interactive experience and maintain reader interest.

                '''
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return chat_completion.choices[0].message.content

def generation(post_type, keywords):
    """
    Generate a post based on the post type and keyword.

    Parameters:
        post_type (int): The type of post to generate.
        keyword (str): The keyword to include in the post.

    Returns:
        str: The generated post.
    """
    if post_type == 1:
        return gen_1(keywords)
    elif post_type == 2:
        return gen_2(keywords)
    elif post_type == 3:
        return gen_3(keywords)
    elif post_type == 4:
        return gen_4(keywords)
    elif post_type == 5:
        return gen_5(keywords)