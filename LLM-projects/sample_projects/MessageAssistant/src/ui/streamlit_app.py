import streamlit as st
from pathlib import Path
import uuid
import sys
import os


# remove the string literal from the path and use the os.path.join method to join the path
project_root = os.path.join(Path(__file__).parent.parent.parent)
sys.path.append(project_root)


def main():
    from src.InformationProcessor.ingestors import SrcIngestor
    from src.DesicionEngine.bot import LLMQAInteraction
    current_file = Path(__file__)
    current_dir = current_file.parent
    SAVE_DIR = current_dir.parent.parent / 'sources'
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    # def calculate_total_steps(uploaded_files):
    #     steps_per_file = 3
    #     return len(uploaded_files) * steps_per_file

    st.set_page_config(page_title="PR Assistant 💬👩‍💼📣")

    with st.sidebar:
        st.title('Public Relations Assistant 💬👩‍💼📣')
        with st.expander("Upload a file"):
            uploaded_files = st.file_uploader("Upload files", type=None, accept_multiple_files=True,
                                              label_visibility='collapsed')
            if uploaded_files:
                st.session_state['uploaded_files'] = uploaded_files

                if 'files_processed' not in st.session_state:
                    fps = [SAVE_DIR / uploaded_file.name for uploaded_file in uploaded_files]
                    for uploaded_file, fp in zip(st.session_state['uploaded_files'], fps):
                        with open(fp, "wb") as f:
                            f.write(uploaded_file.getvalue())
                    memory_bank = "company_data"
                    sess_name = "pdf_extracted_content"
                    id = str(uuid.uuid4())
                    st.session_state['ingestor_params'] = (
                    memory_bank + f"_{id}", sess_name, {"pdf": [str(fp) for fp in fps]})
                    st.session_state['files_processed'] = True

    # API key handling
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai_api = st.secrets['OPENAI_API_KEY']
    else:
        openai_api = st.text_input('Enter Replicate API token:', type='password')
        if openai_api:
            if not (openai_api.startswith('r8_') and len(openai_api) == 40):
                st.warning('Please enter valid credentials!', icon='⚠️')
            else:
                st.success('Proceed to entering your prompt message!', icon='👉')
    if openai_api:
        os.environ['OPENAI_API_KEY'] = openai_api

    # Model selection and parameters
    st.subheader('I can help with press releases, client briefs, and more! 📣👩‍💼💬📰📝')
    selected_model = st.sidebar.selectbox('Choose an Openai model',
                                          ['GPT-4 (Top of the line)', 'GPT-3 (Standard)'],
                                          key='selected_model')
    llm = 'gpt-4-0125-preview' if selected_model == 'GPT-4 (Top of the line)' else 'gpt-3.5-turbo-0125'
    temperature = st.sidebar.slider('Creativity level (temperature)',
                                    min_value=0.001,
                                    max_value=1.0,
                                    value=0.001,
                                    step=0.01)
    max_length = st.sidebar.slider('Max number of tokens (5~ words each)',
                                   min_value=32,
                                   max_value=1000,
                                   value=350,
                                   step=8)

    # Initialize chat messages
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    def generate_llm_response(prompt_input):
        if 'ingestor_params' in st.session_state and 'files_processed' in st.session_state:
            memory_bank, sess_name, file_sources = st.session_state['ingestor_params']
            # Initialize ingestor only if files are processed and ingestor not yet initialized
            if 'ingestor_initialized' not in st.session_state:
                ingestor = SrcIngestor(memory_bank, sess_name, file_sources, openai_api=openai_api)
                ingestor.file_broker()  # Process files only once
                st.session_state['ingestor_initialized'] = True  # Mark ingestor as initialized after processing

            string_dialogue = ""
            for dict_message in st.session_state.messages:
                string_dialogue += f"{dict_message['role']}: {dict_message['content']}\n\n"

            stm_path = os.path.join(current_dir, '..', 'STM')
            llm_qa = LLMQAInteraction(openai_api,
                                      stm_path,
                                      memory_bank,
                                      sess_name,
                                      temperature=temperature,
                                      llm_model_name=llm,
                                      max_tokens=max_length)
            output = llm_qa.ask_question(prompt_input)
            return output
        else:
            return "Ingestor is not initialized or files not processed."

    if prompt := st.chat_input(disabled=not openai_api):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_llm_response(prompt)
                    formatted_response = response.content.replace('\n', '\n\n')
                    print(formatted_response)
                    placeholder = st.empty()
                    full_response = formatted_response
                    placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
