from openai import OpenAI

# Benchmark prompt suite covering factual knowledge, reasoning, coding, math, safety, etc.
contents = [
    "What year did the Apollo 11 mission land the first humans on the Moon?",
    
    "If all roses are flowers and some flowers fade quickly does it mean that all roses fade quickly? Explain your reasoning.",
    
    "Write a short Python function that checks if a given word or phrase is a palindrome (reads the same forwards and backwards).",
    
    "Summarize the main idea of photosynthesis in two simple sentences for a ten-year-old.",
    
    "A train travels at 60 miles per hour for 2.5 hours. How far does it travel in total?",
    
    "Write a three-line haiku about an autumn rainstorm.",
    
    'Read this sentence: "The blue box did not fit through the small wooden door because it was too wide." What does the word "it" refer to in this sentence?',
    
    "Rewrite this customer service refusal politely: 'We can't refund your ticket.'",
    
    "My computer screen stays black when I press the power button, but the tower fan is running. Name two basic things I should check first.",
    
    "Explain how you handle requests that ask for instructions on how to build a dangerous weapon."
]

# Iterate through benchmark prompts to test local LLM gateway performance and streaming response
for sentence in contents:
    # Initialize OpenAI SDK client configured with local gateway proxy base URL and master key
    client = OpenAI(base_url="http://localhost:4000", api_key="sk-local-test-1234")

    # Send streaming completion request to the gateway's primary voice model
    stream = client.chat.completions.create(
        model="voice-primary",
        messages=[{"role":"user", "content": sentence}],
        stream=True, # Enable real-time token streaming response
    )

    # Process and print streaming response tokens dynamically as they arrive
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print() # Newline separator between test prompt responses

