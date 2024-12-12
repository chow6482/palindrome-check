from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import config

# 1. Create the model
model = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY)

# 2. Create the function to check for palindrome
def is_palindrome(word: str) -> str:
    """
    Checks if a word is a palindrome.
    A palindrome is a word that reads the same forwards and backwards.
    """
    clean_word = ''.join(char.lower() for char in word if char.isalnum())  # Remove non-alphanumeric chars and lowercase it
    is_palindrome = clean_word == clean_word[::-1]  # Check if the word is equal to its reverse
    return "Yes, it is a palindrome." if is_palindrome else "No, it is not a palindrome."

# 3. Create the tools
tools = [
    Tool.from_function(
        func=is_palindrome,
        name="Check Palindrome",
        description="Check if a given word is a palindrome",
    )
]

# 4. Get the prompt to use
prompt = hub.pull("hwchase17/react", api_key=config.LANGSMITH_API_KEY)  # Ensure API key is in the config module

# 5. Construct the ReAct agent
agent = create_react_agent(model, tools, prompt)

# 6. Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 7. Invoke the agent executor with an example input
input_word = "radar"  # Change this to test with other words
result = agent_executor.invoke({"input": f'Is the word "{input_word}" a palindrome?'})

# 8. Print the result
print("Result:", result)
