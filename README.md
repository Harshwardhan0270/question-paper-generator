# Question Paper Generator

This is a Streamlit web application that generates question papers based on Bloom's Taxonomy. It uses the Groq API via Langchain to generate multiple-choice questions (MCQs), short answer questions, and long answer questions.

## Features

- Generate MCQs, short answer, and long answer questions based on subject and syllabus input.
- Supports Bloom's Taxonomy levels for question difficulty.
- Download generated questions as a DOCX file.
- Uses environment variable `GROQ_API_KEY` for API authentication.

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set the environment variable `GROQ_API_KEY` with your Groq API key.
5. Run the app:
   ```
   streamlit run app.py
   ```

## Deployment

You can deploy this app on Streamlit Cloud or other platforms that support Streamlit apps. Make sure to set the `GROQ_API_KEY` environment variable in the deployment settings.

## License

This project is licensed under the MIT License.
