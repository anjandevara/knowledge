import os
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if "approved_stories" not in st.session_state:
    st.session_state.approved_stories = []
if "page" not in st.session_state:
    st.session_state.page = "Generate"

PAGE_OPTIONS = ["Generate", "Approved Stories"]
page = st.sidebar.radio("Navigation", PAGE_OPTIONS, key="page")

PRE_PROMPT = (
    "You are an assistant that converts user stories into Gherkin format. "
    "Return only the Gherkin text."
)


def call_openai(story: str) -> str:
    """Convert a user story into Gherkin using OpenAI."""
    messages = [
        {"role": "system", "content": PRE_PROMPT},
        {"role": "user", "content": story},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"].strip()


if page == "Generate":
    st.title("User Story to Gherkin")

    story = st.text_area(
        "User Story",
        value=st.session_state.get("story_text", ""),
        height=200,
    )

    generate = st.button("Generate Gherkin")
    if generate and story.strip():
        st.session_state.story_text = story
        with st.spinner("Contacting OpenAI..."):
            st.session_state.gherkin = call_openai(story)
    elif generate:
        st.warning("Please enter a user story first.")

    if "gherkin" in st.session_state:
        st.subheader("Generated Gherkin")
        st.code(st.session_state.gherkin)
        col1, col2 = st.columns(2)
        if col1.button("Approve"):
            st.session_state.approved_stories.append(st.session_state.gherkin)
            st.session_state.page = "Approved Stories"
            st.session_state.pop("gherkin", None)
            st.session_state.pop("story_text", None)
            st.experimental_rerun()
        if col2.button("Regenerate"):
            with st.spinner("Regenerating..."):
                st.session_state.gherkin = call_openai(story)

elif page == "Approved Stories":
    st.title("Approved Stories")
    stories = st.session_state.approved_stories
    if stories:
        for idx, text in enumerate(stories, 1):
            st.subheader(f"Story {idx}")
            st.code(text)
        csv_content = "story\n" + "\n".join(stories)
        st.download_button(
            "Download CSV",
            csv_content,
            file_name="stories.csv",
            mime="text/csv",
        )
        txt_content = "\n\n".join(stories)
        st.download_button(
            "Download TXT",
            txt_content,
            file_name="stories.txt",
            mime="text/plain",
        )
    else:
        st.info("No stories have been approved yet.")

