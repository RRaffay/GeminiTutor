from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load the environment file
load_dotenv()

# Access environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
model_pro = genai.GenerativeModel('gemini-1.5-pro-latest')


def main():
    """
    Main function to test the Gemini API.
    """
    # for m in genai.list_models():
    #     if 'generateContent' in m.supported_generation_methods:
    #         print(m.name)

    input = "Hello, how are you today?"
    print(model_pro.generate_content(input).text)


if __name__ == "__main__":
    main()
