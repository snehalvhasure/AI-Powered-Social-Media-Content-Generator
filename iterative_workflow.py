import langchain
import langgraph
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from typing import TypedDict, Literal
from pydantic import BaseModel, Field

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check whether API keys are available
if not GROQ_API_KEY or not OPENAI_API_KEY:
    raise ValueError("API keys are missing. Please check your .env file.")

generator_llm = ChatOpenAI(model = "gpt-4o-mini")
evaluator_llm = ChatGroq(model = "openai/gpt-oss-20b")
optimizer_llm = ChatOpenAI(model = "gpt-4o")

# Evaluate Class
class TextEvaluation(BaseModel):
    evaluate : Literal["approved", "improvement"] = Field(description = "Final Evaluate of Output: ")
    feedback : str = Field(description = "Feedback of the text Generated.")

structured_evaluator_llm = evaluator_llm.with_structured_output(TextEvaluation)
print("\n\nStructured Evaluator LLM: ", structured_evaluator_llm)

msg = """War brings destruction, not solutions.
Innocent lives should never pay the price of conflict.
Choose peace over hatred, dialogue over violence.
No nation wins when humanity loses.
Praying for peace between Iran and the USA."""

messages = [
    SystemMessage(content = "You must use the TextEvaluation tool to provide your evaluation and feedback. Do not respond with plane conversational text."),
    HumanMessage(content = msg)
]
try:
    response = structured_evaluator_llm.invoke(messages)
    print(response)
except Exception as e:
    print(f"An error occured: {e}")
    print("\n\nTip: If the model continues to fail tool calling, consider switching the evaluatior_llm to an OpenAI model (like 'gpt-4o-mini') which has more robust tool-calling capabilities.")

# STATE
class ContentState(TypedDict):
    topic : str
    text : str
    evaluation : Literal["approved", "improvement"]
    feedback : str
    iteration : int
    max_iteration : int

def generate_node(state: ContentState):
     """Generates a social media tweet based on the topic provided by the user."""

     topic = state["topic"]
     prompt1 = f"""You are a polite, intelligent and clever content writer which can posted on social media website like Twitter, Facebook, etc.
               Generate a social media tweet based on the following topic provided by the user. {topic}

               Rules to follow:
               1. Maximum length of tewwt should not exceed 200 characters.
               2. Add some humor in the tweet which people talk about things in daily life.
               3. Do not use question-answer format.
               4. Use simple English to frame the tweet.
               5. End the post with some strong punchline along with funny statement."""

     response1 = generator_llm.invoke(prompt1).content
     return {"text" : response1} 

def evaluation_node(state: ContentState):
      """This evaluates the tweet based on context, humor, orginality, length and generates the final approval."""
      
      topic = state["topic"]
      text = state["text"]

      prompt2 = f"""You are an intelligent and clever content evaluator and critic.

                Evaluate the following cintent provided below based on paramaters like content, humor, originality, sarcasm, etc. which is based on {topic}
                content: {text}

                Use following criteria to evaluate the content:
                1. Originality - Evaluate this content is fresh and new
                2. Humor - Did this content make you smile, laugh, or happy?
                3. Attractive - Is content is relevant, sttractive, sharp, short?
                4. Share - Would people believe and share it in their contacts?
                5. Format - Is the content well rganized and formatted within 200 characters?

                Auto-reject if:
                1. If content is in Question-Answer format
                2. If the content exceed over 200 characters
                3. If it is a repeated content which appear more times
                4. If the content is non-relevant to the topic.

                Respond only in Pre-defined Structured Format:
                1 Evaluation : "approved" or "improvement"
                2. feedback : "generate one paragraph explaining the pros and corns of the content."""

      response2 = structured_evaluator_llm.invoke(prompt2)
      return {"evaluation" : response2.evaluate, "feedback" : response2.feedback}

def optimizer_node(state: ContentState):
     feedback = state["feedback"]
     topic = state["topic"]
     text = state["text"]

     prompt3 = f"""You are an intelligent and clever content generator based on content, organility, sarcasm, humor, etc
                Re-generate content based on following topic by enhancing the quality considering feedback below:
                1. Feedback : {feedback}
                2. Topic : {topic}
                3. Text : {text}"""
     response3 = optimizer_llm.invoke(prompt3)
     iteration = state["iteration"]

     return {"text" : response3, "iteration" : iteration}

def condition_route(state: ContentState) -> Literal["approved", "improvement"]:
     if state["evaluation"] == "approved" or state["iteration"] >= 5:
          return "approved"
     else:
          return "improvement"

# GRAPH

graph = StateGraph(ContentState)
graph.add_node("generate_node", generate_node)
graph.add_node("evaluation_node", evaluation_node)
graph.add_node("optimizer_node", optimizer_node)

# Add edges between nodes
graph.add_edge(START, "generate_node")
graph.add_edge("generate_node", "evaluation_node")
graph.add_conditional_edges("evaluation_node", condition_route, {"approved": END, "improvement": "optimizer_node"})
graph.add_edge("optimizer_node", "evaluation_node")

iter_workflow = graph.compile()
print("\nCompiled Iterative Workflow: ", iter_workflow)

# we need 3 inputs which we used in 'class ContentState(TypedDict)'
# 1. topic, 2. iteration, 3. max_iteration
input_data = {"topic": "India", "iteration": 1, "max_iteration": 5}
result = iter_workflow.invoke(input_data)
print("\n\nResult: ", result)