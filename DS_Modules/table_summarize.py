import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser #Takes Ouptput from model and convert it into string

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def table_summarize(data_category):
    prompt_text = """You are assistant tasked with summarizing the tables. \
        Give a concise summary of the table.Table chunks : {element}"""
    
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOpenAI(temperature = 0,model = "gpt-3.5-turbo",api_key=openai_api_key)
    summarize_chain = {"element":lambda x:x}|prompt|model|StrOutputParser
    table_summaries = summarize_chain.batch(table,{"max_concurrency": 5})

    return table_summaries

table_summarize = table_summarize()
