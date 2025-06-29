# Watsonx Scribe

> Your AI-powered assistant for instant meeting insights.

Watsonx Scribe is a web application developed for the `AI & Automation Unpacked Hackathon`. It's designed to transform lengthy meeting recordings into a searchable and interactive knowledge base, helping users to quickly find the information they need without re-watching hours of video.

## ✨ The Idea

In any organization, crucial information and key decisions are often made during meetings. While these sessions are recorded, the knowledge within them remains "trapped." Finding a specific detail requires manually scrubbing through audio or video files, which is inefficient and time-consuming.

Our project, Watsonx Scribe, aims to solve this problem. We provide a simple platform where users can upload a meeting recording and instantly start asking questions in natural language to get precise, fact-based answers.

## 🚀 How It Works

The application follows a simple yet powerful two-stage AI pipeline:

1.  **Upload & Transcribe:** A user uploads their meeting audio or video file. The application leverages a state-of-the-art speech-to-text model to generate a highly accurate and readable transcript.
2.  **Ask & Answer:** The generated transcript is then used as the foundational context for our Q&A engine. The user can ask questions through a chat interface, and the AI provides answers grounded exclusively in the content of that meeting.

## 🧠 The AI Core

Our solution integrates two distinct AI models to achieve its goal:

### Transcription Engine
* **Model:** OpenAI Whisper (`base` model).
* **Reasoning:** We chose Whisper for its exceptional accuracy across various languages and accents. Its ability to run locally provides a robust and cost-effective solution for the transcription stage, which is a critical first step for our pipeline.

### Q&A Reasoning Engine
* **Platform:** IBM watsonx.ai
* **Model:** `ibm/granite-13b-instruct-v2`
* **Usage:** The Granite model is the heart of our application. It receives the full meeting transcript as context, along with the user's question and a carefully engineered set of instructions. Its primary task is to perform reliable, extractive question-answering. Through specific prompt engineering, we've guided the model to **only** use the information present in the transcript, ensuring factual accuracy and preventing AI hallucination. It is explicitly instructed to state when an answer cannot be found.

## 🔧 Getting Started

To run this project locally, please follow these steps.

### Prerequisites
* Python 3.8+
* `ffmpeg`: This is a dependency for the Whisper model. You can install it from [ffmpeg.org](https://ffmpeg.org/download.html).

### Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/watsonx-scribe.git](https://github.com/your-username/watsonx-scribe.git)
    cd watsonx-scribe
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a `requirements.txt` file from your environment using `pip freeze > requirements.txt`)*

### Configuration
1.  Open the `app.py` file.
2.  Find the following lines and replace the placeholder text with your actual credentials:
    ```python
    API_KEY = "YOUR_IBM_CLOUD_API_KEY"
    PROJECT_ID = "YOUR_WATSONX_PROJECT_ID"
    ```

### Running the Application
1.  Open your terminal in the project directory.
2.  Run the following command:
    ```bash
    streamlit run app.py
    ```
3.  Your web browser will automatically open with the application running.

## Demo

### Sample Video

Our demonstration uses a sample meeting audio extracted from the following source:
-   **Source:** `https://www.youtube.com/watch?v=3WrZMzqpFTc`
-   **Topic:** A weekly Student Success meeting discussing student absenteeism and well-being.

## 🧪 Sample Questions

Here are some sample questions you can use to test the application with the provided transcript:

1.  What is the proposed solution to encourage students to come to school on Fridays?
2.  Why has John Smith been absent from school?
3.  What are the two main actions that were decided upon to address student issues?
4.  What were the two main problems discussed in the meeting?
5.  What is the school's budget for the pancake breakfast? (This question tests the model's ability to identify missing information).
