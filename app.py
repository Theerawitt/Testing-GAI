
import streamlit as st
from transformer import GPT2Tokenizer, GPT2LMHeadModel

#Load  pre trained GPT2 model and tokenizer 
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

#Ensure that EOS token is present 
if tokenizer.eos_token is None:
    tokenizer.add_special_tokens({'eos_token': '<|endoftext|>'})
    model.resize_token_embeddings(len(tokenizer))

#Define response generation function 
def generate_reponse(user_input, max_length = 100):
    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    response_ids = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_p=0.9,
        temperature=0.7
    )
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response

#Streamlit web app
st.title("GPT-2 chatbot")
st.write("A simple chatbot built with GPT-2. Say what you want")

#Input text boxfor user
user_input = st.text_input("You:")

#When input is given, generate a response
if user_input:
    with st.spinner("Im typing. Wait"):
        response =generate_response(user_input)
    st.write(f"Chatbot: {response}")
        