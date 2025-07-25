# knowledge

This repository includes a small Streamlit application that converts user
stories into Gherkin format using the OpenAI API. The app allows you to
generate, review and store Gherkin stories, and to export approved stories
as CSV or plain text files.

## Running the app

1. Create a `.env` file and define your `OPENAI_API_KEY`.
2. Install the required dependencies:

   ```bash
   pip install streamlit openai python-dotenv
   ```

3. Start the application:

   ```bash
   streamlit run app.py
   ```

Use the sidebar to navigate between generating a new story and viewing your
approved stories.
