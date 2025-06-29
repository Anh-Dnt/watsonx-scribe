import streamlit as st
import os
import whisper
from ibm_watson_machine_learning.foundation_models import Model # For Step 2
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

# --- 2. CONFIGURE YOUR CREDENTIALS ---
API_KEY = "Your api key"
PROJECT_ID = "Your project id"
MODEL_ID = "ibm/granite-13b-instruct-v2"

# --- 3. HELPER FUNCTIONS ---

# Function for Step 1: Transcribe Audio using Whisper
@st.cache_data # Use Streamlit's cache to avoid re-transcribing the same file
def transcribe_audio(audio_file_path):
    """
    Loads the Whisper model and transcribes the given audio file.
    """
    st.write("Loading Whisper model...")
    model = whisper.load_model("base") # 'base' model is fast and efficient
    st.write("Model loaded. Starting transcription...")
    result = model.transcribe(audio_file_path, fp16=False)
    st.write("Transcription complete.")
    return result["text"]

# Function for Step 2: Ask the Q&A Bot on watsonx.ai
@st.cache_data # Cache the answers for the same questions
def ask_qna_bot(_transcript_content, question): # Use _transcript_content to make caching work
    """
    This function sends the transcript and a question to the watsonx.ai model.
    """
    # --- MODEL PARAMETERS ---
    parameters = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.MAX_NEW_TOKENS: 512,
        GenParams.REPETITION_PENALTY: 1.05,
        GenParams.STOP_SEQUENCES: ["---"]
    }

    # --- SETUP THE MODEL ---
    credentials = { "url": "https://us-south.ml.cloud.ibm.com", "apikey": API_KEY }
    model = Model(model_id=MODEL_ID, params=parameters, credentials=credentials, project_id=PROJECT_ID)

    # --- CREATE THE PROMPT ---
    prompt_template = f"""
You are a helpful, comprehensive, and precise meeting assistant.
Your task is to answer questions based ONLY on the provided meeting transcript.
- Provide a complete and detailed answer, including all relevant information mentioned in the transcript.
- SPECIAL INSTRUCTION FOR SUMMARIZATION: To identify the main topic or purpose of the meeting, first identify the core problem being discussed, then list the proposed solutions. The main topic is the core problem itself. Synthesize this into a concise answer.
- If the answer cannot be found in the transcript, you must respond with "I'm sorry, that information is not available in the meeting transcript."

--- TRANSCRIPT ---
{_transcript_content}
--- END TRANSCRIPT ---

--- QUESTION ---
{question}
--- END QUESTION ---

Answer:
"""
    # --- GENERATE RESPONSE ---
    generated_response = model.generate(prompt=prompt_template)
    answer = generated_response['results'][0]['generated_text']
    return answer

# --- 4. STREAMLIT APPLICATION UI ---

st.set_page_config(page_title="Watsonx Scribe", layout="wide")

st.title("🎙️ Watsonx Scribe")
st.write("Powered by OpenAI Whisper & IBM Granite on `watsonx.ai`")

# --- Initialize session state ---
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Upload your meeting audio or video file (MP3, WAV, MP4...)",
    type=['mp3', 'wav', 'mp4', 'm4a']
)

if uploaded_file is not None:
    # Save the uploaded file temporarily to process it
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process the file only once
    if not st.session_state.processing_done:
        with st.spinner("Processing audio... This might take a few minutes for the first run."):
            st.session_state.transcript = transcribe_audio(file_path)
            st.session_state.processing_done = True
        st.success("File processed successfully!")

    # --- Display Transcript and Q&A section ---
    if st.session_state.transcript:
        st.header("Meeting Transcript")
        st.text_area("Transcript", st.session_state.transcript, height=250)

        st.header("Ask a Question")
        user_question = st.text_input("Enter your question about the meeting:")

        if user_question:
            with st.spinner("Thinking..."):
                answer = ask_qna_bot(st.session_state.transcript, user_question)
                st.info(f"**Question:** {user_question}\n\n**Answer:** {answer}")

# Reset button to allow processing a new file
if st.button("Process a New File"):
    st.session_state.processing_done = False
    st.session_state.transcript = ""
    st.experimental_rerun()
