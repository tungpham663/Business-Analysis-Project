from api_key import API_KEY
from groq import Groq

client = Groq(api_key=API_KEY)
MODEL = "llama-3.3-70b-versatile"

def eval(generated_text, query, input_data, model=MODEL, temperature=0.3, max_tokens=2000):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'You are tasked with evaluating the quality of a generated tweet across multiple criteria.'
            },
            {
                'role': 'user',
                'content': f'''
You are tasked with evaluating the quality of a generated tweet across multiple criteria. Assign a score from 1 to 5 for each criterion based on the definitions provided below and explain your reasoning briefly.

User query: {query}  
Input data: {input_data}  
Generated tweet: {generated_text}  

Scoring criteria: 
Response Appropriateness (Relevant to User Query): Does the tweet directly answer or fulfill the user's query?
- 5: Fully satisfies the query with accurate, relevant, and complete information.
- 4: Mostly satisfies the query but may lack minor details.
- 3: Partially satisfies the query; some key aspects are missing or vague.
- 2: Poorly satisfies the query; most aspects are irrelevant or incorrect.
- 1: Does not satisfy the query at all or is entirely irrelevant.

Relevance to Input Data: Does the tweet reflect accurate and relevant information from the input data?
- 5: All details align perfectly with the input data.
- 4: Most details are accurate and relevant but may miss minor aspects.
- 3: Partially aligns; some inaccuracies or irrelevant elements are present.
- 2: Poor alignment; most details are inaccurate or irrelevant.
- 1: No alignment with the input data at all.

Clarity, Conciseness, and Coherence: Is the tweet easy to understand, free of unnecessary information, and logically structured?
- 5: Extremely clear, concise, and coherent with no ambiguity or redundancy.
- 4: Mostly clear, concise, and coherent but with minor areas for improvement.
- 3: Somewhat clear and coherent but contains noticeable ambiguity, redundancy, or disjointed flow.
- 2: Poor clarity and cohesion; verbose or lacks logical flow.
- 1: Completely unclear, verbose, or incoherent.

Uniqueness: Does the tweet contain novel and original content?
- 5: Entirely unique and creative.
- 4: Mostly unique but has some familiar elements.
- 3: Partially unique; contains common or repetitive ideas.
- 2: Poor uniqueness; mostly repetitive or generic.
- 1: Completely unoriginal or copied.

Visual Content: Does the tweet suggest or effectively integrate visual elements (e.g., emojis, images, or videos)?
- 5: Perfect use of visual elements to enhance the tweet.
- 4: Effective use of visuals but could be optimized further.
- 3: Some visual elements are present but not effective.
- 2: Poor use of visuals; ineffective or irrelevant.
- 1: No visual content included when it would have been helpful.

Hashtag Usage: Are hashtags used appropriately and effectively to enhance discoverability?
- 5: Perfect hashtag usage; relevant, concise, and impactful.
- 4: Mostly appropriate but could include better or additional hashtags.
- 3: Somewhat appropriate but includes irrelevant or excessive hashtags.
- 2: Poor usage; hashtags are irrelevant or missing.
- 1: No hashtags included when they would have been beneficial.

Informational Content: Does the tweet provide valuable or meaningful information?
- 5: Highly informative and valuable.
- 4: Mostly informative but lacks minor details.
- 3: Partially informative; some valuable points but incomplete.
- 2: Poorly informative; most content is irrelevant or vague.
- 1: Not informative at all.

Engagement Potential: Does the tweet encourage user interaction (e.g., calls to action, questions, or polls)?
- 5: Highly engaging with strong calls to action.
- 4: Mostly engaging but could be improved.
- 3: Somewhat engaging but lacks impactful elements.
- 2: Poor engagement potential; unappealing for interaction.
- 1: No engagement potential at all.

Instructions:
- For each criterion, assign a score from 1 to 5 and provide a brief explanation for your decision.

Output format:
- Response Appropriateness: [1-5] - [Explanation]
- Relevance to Input Data: [1-5] - [Explanation]
- Clarity, Conciseness, and Coherence: [1-5] - [Explanation]
- Uniqueness: [1-5] - [Explanation]
- Visual Content: [1-5] - [Explanation]
- Hashtag Usage: [1-5] - [Explanation]
- Informational Content: [1-5] - [Explanation]
- Engagement Potential: [1-5] - [Explanation]'''
            }
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return chat_completion.choices[0].message.content
