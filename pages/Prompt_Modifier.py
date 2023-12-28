import streamlit as st

# Read the prompts from the file
with open('prompts.txt', 'r') as file:
    prompts = file.read().split('---')

quality_prompt = prompts[0].strip()
quantity_prompt = prompts[1].strip()

# Display the text areas for the prompts
st.subheader("Quality Prompt")
quality_prompt = st.text_area("", quality_prompt,height=400)
save_quality = st.button('Save Quality Prompt')
# Display the buttons to save the prompts
if save_quality:
    prompts[0] = quality_prompt
    with open('prompts.txt', 'w') as file:
        file.write('---'.join(prompts))
    st.success('Quality prompt saved!')

st.subheader("Quantity Prompt")
quantity_prompt = st.text_area("", quantity_prompt,height=440)
save_quantity = st.button('Save Quantity Prompt')
if save_quantity:
    prompts[1] = quantity_prompt
    with open('prompts.txt', 'w') as file:
        file.write('---'.join(prompts))
    st.success('Quantity prompt saved!')
