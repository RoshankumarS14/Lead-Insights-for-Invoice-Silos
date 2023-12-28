import streamlit as st
import os

st.set_page_config(
    page_title="File Uploader",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown('''
    <style>
    .element-container {
        background-color: #a19e9e;
        opacity: 1;
    }
    .st-b7 {
        color: white;
    }
    .css-nlntq9 {
        font-family: Source Sans Pro;
    }
    </style>
''', unsafe_allow_html=True)

def replace_file(file):
    # Specify the directory where the file exists
    directory = '.'  # Current directory (you can change this to your desired directory)

    # Check if the uploaded file exists
    if os.path.exists(os.path.join(directory, file.name)):
        # Remove the existing file
        os.remove(os.path.join(directory, file.name))

        # Save the uploaded file in the same directory with the same name
        with open(os.path.join(directory, file.name), 'wb') as f:
            f.write(file.getvalue())
        
        st.success(f"File '{file.name}' replaced successfully!")
    else:
        st.warning(f"File '{file.name}' does not exist in the directory.")

def main():
    st.title("Replace File in Current Directory")

    # Display a file uploader widget
    uploaded_file = st.file_uploader("Upload a file to replace", type=["xlsx"])

    # Check if a file was uploaded
    if uploaded_file is not None:
        replace_file(uploaded_file)

if __name__ == "__main__":
    main()
