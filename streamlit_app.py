import cohere
import streamlit as st

# Prompt for Cohere API key
cohere_key = st.text_input("Enter your Cohere API key:", type="password")

# Initialize Cohere client only if API key is provided
if cohere_key:
    co = cohere.Client(cohere_key)
else:
    co = None
    st.warning("Cohere API key not provided. Analysis features will not be available.")

# Initialize 'ideas' and 'analysis' in session state if they don't exist
if 'ideas' not in st.session_state:
    st.session_state['ideas'] = []
if 'analysis' not in st.session_state:
    st.session_state['analysis'] = None

def analyze_ideas():
    """
    Analyzes stored ideas using Cohere and updates analysis state.
    """
    if st.session_state['ideas']:
        newline = "\n"
        prompt = f"""Analyze a list of brainstorming ideas and identify key themes, patterns, and potential new directions.

Ideas:

{newline.join(st.session_state['ideas'])}
        """ 

        response = co.generate(
            model="command",
            prompt=prompt,
            max_tokens=60,
            temperature=0.7,
            k=0,
            stop_sequences=["--"],
        )

        analysis = response.generations[0].text.strip()
        st.session_state['analysis'] = analysis

st.title("Group Brainstorming Tool")

# Create 5 input fields for new ideas
idea_inputs = [""] * 5  # Initialize list to store 5 ideas
for i in range(5):  # Create 5 input fields
    idea_inputs[i] = st.text_input(f"Add idea #{i+1}:", placeholder=f"Write idea #{i+1} here", key=f'idea_{i}')

# Add button to submit new ideas
if st.button("Add Ideas"):
    # Check if at least one idea is entered
    if any(idea_inputs):
        # Append each non-empty idea to the session state
        for idea in idea_inputs:
            if idea:  # Ensure the idea is not empty
                st.session_state['ideas'].append(idea)
        st.success("Ideas added!")
        analyze_ideas()
    else:
        st.error("Please enter at least one idea.")

# Display list of submitted ideas
if st.session_state['ideas']:
    st.header("Brainstorming Ideas:")
    for idea in st.session_state['ideas']:
        st.markdown(f"- {idea}")

# Analyze and display insights
if st.session_state['analysis']:
    st.header("Analysis:")
    st.write(st.session_state['analysis'])

st.markdown("---")
st.info("Note: This app uses Cohere API for idea analysis. It is recommended to have a Cohere API key for optimal performance.")
