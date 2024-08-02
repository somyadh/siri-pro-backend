# app/utils.py
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

def create_llm():
    llm = Ollama(model="llama3")
    return llm

def execute_prompt(llm, prompt_text):
    output_parser = StrOutputParser()
    result = llm(prompt_text)
    parsed_result = output_parser.parse(result)
    return parsed_result