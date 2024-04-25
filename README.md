# Gemini Tutor

## Goal

The goal is of this project is to try to test the feasibility of using a chatbot to help students in learning. More specifically, the chatbot can help the students by understanding how much they know about a topic and then provide them with the necessary resources to help them learn more about the topic. Since the chatbot remembers the student's progress, it can also provide the student with personalized questions to test whether progress has been made.

## Setup and Run Project

1. **Create a virtual environment**
   Use the following command to create a new virtual environment named 'venv':

   ```sh
   python3 -m venv .venv
   ```

2. **Activate the virtual environment** On Windows, use the following command:

   ```sh
   .\.venv\Scripts\activate
   ```

   On Unix or MacOS, use the following command:

   ```bash
   source .venv/bin/activate
   ```

3. **Configure Firebase and Gemini Credentials** Get the `googleCreds.json` file from firebase. Once you have it, place it in the project root directory. Also get the API key for Gemini and place it in the `app/gemini_funcs` directory in a `.env` file.

4. **Install the required packages** Use the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application** Use the following command to run the Flask application:

   ```bash
   python run.py
   ```

The application will start running at `http://127.0.0.1:5000/`.
