import streamlit as st
import numpy as np
import pandas as pd
import os
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI

st.set_page_config(
    page_title="Leads Insights",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.image("logo.png")
df = pd.read_excel("ArcaData-TestData.xlsx")
df = df.loc[:,:"CLF"].iloc[:-1]

invoice_budget = dict(pd.pivot_table(df,"Budget","Invoice",aggfunc=sum)[:].reset_index().values)
silo_ap_rating = {"S01": 5,"S02": 6,"S03": 4,"S04": 3,"S05": 5,"S06": 5,"S07": 7,"S08": 7,"S09": 7,"S26": 8,"S28": 7,"S30": 2,"S41": 5,"H01": 8}

df["Elap-C/Dur-C"] = round(df["Elap-C"]/df["Dur-C"]*100,2)
df["Elap-Budget"] = round(df["Elap-C/Dur-C"]*df["Budget"]/100,2)
df["Total Budget for Invoice"] = df["Invoice"].apply(lambda a : invoice_budget[float(a)])
df["AP Rating"] = df["Silo"].apply(lambda a : silo_ap_rating[a] if a in silo_ap_rating.keys() else 5)
df["APLM"] = df["AP Rating"]/5*100
df["Lead Equivelency Based on AP Rating"] = round(df["APLM"]*df["Ad-Leads"]/100)
df["CPL-LE"] = df[["Budget","Lead Equivelency Based on AP Rating"]].apply(lambda a : round(a[0]/a[1],2) if a[1]!=0 else 0,axis=1)
df["R-Budget"] = df["Budget"] - df["Elap-Budget"]
df["Shift To"] = df["CLF"].apply(lambda a : "Quality" if a>1 else "Quantity")

invoice = st.selectbox("Select the invoice:",df["Invoice"].unique())
insight_type = df[df["Invoice"]==invoice]["Shift To"].values[0]
invoice_df = df[df["Invoice"]==invoice][["Silo","APLM","CPL-LE","R-Budget"]].sort_values(["Silo"]).reset_index(drop=True)
openai_key = "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"
chat = ChatOpenAI(openai_api_key=openai_key,model="gpt-4-1106-preview")

df_html = invoice_df.to_html(classes='table table-striped')
df_html = df_html.replace('<table ','<table style="text-align:right; margin-bottom:40px; margin-top:50px;" ')
st.markdown(df_html, unsafe_allow_html=True)

insights = st.button("Generate Insights")

if insights:

    if insight_type=="Quality":
        template="You are a brilliant strategist with a knack for statistical analysis. Your goal is to perfectly adjust the budgets for the following media campaigns to help the client achieve maximum quality. Quality is indicated in the column labeled ‘APLM’. The ‘CPL-LE’ column is considered good if it is low and bad if it is high. Silos S44, S09, and S07 should NOT be factored in, regardless of their data. To accomplish your goal, examine the performance of the other silos. Identify silos with the lowest ‘APLM’ and the highest ‘CPL-LE’. If they are performing significantly worse—meaning their ‘CPL-LE’ is the same or higher than the two with the highest ‘APLM’—suggest reallocating their ‘R-Budget’ to the two silos performing the same or better but with a higher ‘APLM’. Exclude S44, S09, or S07 from this shift. Determine the shift amount based on the performance difference. For a significant difference, shift up to two-thirds of the budget; for a smaller difference or if they are the same, shift at least one-third. Even if a silo's performance is the same or slightly worse but has a significantly higher ‘APLM’, it is beneficial to shift funds into that silo, as the goal is to improve quality. Provide a very brief paragraph with your recommendation in no more than two sentences without bullet points, specifying exact numbers. After your explanation, a summary is helpful."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template="{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    else:
        template="You are a brilliant strategist with a knack for statistical analysis. Your goal is to perfectly adjust the budgets for the following media campaigns to help the client achieve the maximum number of leads. Quality is indicated in the column labeled ‘APLM’. The ‘CPL-LE’ column is considered good if it is low and bad if it is high. Silos S44, S09, and S07 should NOT be factored in, regardless of their data. To accomplish your goal, examine the performance of the other silos. Look for Silos with the lowest ‘CPL-LE’ which indicates the cost per lead is lower and thus it is a well performing silo. For this purpose, we want to shift money from silos with high ‘CPL-LE’ over to once with lower ‘CPL-LE’. It is best to pick the two worst performers and then shift to the two best performers based on this criterion. Do not feel compelled to do two if circumstances warrant fewer, or more, but simply use two as the benchmark. Also, while the purpose of this exercise is to shift funds to well performing silos, do take into consideration that quality is of utmost importance. We do not want to make shifts when things are close. In close situations it is better to stay the course than shift out of silos with high ‘APLM’ even if they are performing slightly lower than others. Remember to exclude S44, S09, or S07 from this shift. Determine the shift amount based on the performance difference. For a significant difference, shift up to two-thirds of the budget; for a smaller difference or if they are the same, shift at least one-third. Provide a very brief paragraph with your recommendation in no more than two sentences without bullet points, specifying exact numbers. After your explanation, a summary is helpful."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template="{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        

    # get a chat completion from the formatted messages
    response = chat(chat_prompt.format_prompt(text=invoice_df.to_json(orient='records')).to_messages())
    # st.write("Input:"+"\n"+str(chat_prompt.format_prompt(text=invoice_df.to_json(orient='records')).to_messages()))
    st.write(response.content.replace("$", "\\$"))


    






















