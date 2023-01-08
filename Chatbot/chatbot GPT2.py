import os
import openai

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "Write a tagline about a ninja in english"

response = openai.Completion.create(
  engine="text-davinci-002",
  #prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman:  What can I do for you? Is there something specific you would like help with?",
  temperature=0.9,
  max_tokens=150,
  #top_p=1,
  #frequency_penalty=0,
  #presence_penalty=0.6,
  #stop=[" Human:", " AI:"]
)

print(response)