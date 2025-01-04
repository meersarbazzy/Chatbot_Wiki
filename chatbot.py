import streamlit as st
from streamlit_chat import message
import wikipedia

# Predefined Q&A dictionary
predefined_responses = {
    "What is Artificial Intelligence?": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are designed to think and learn.",
    "What is Machine Learning?": "Machine Learning is a subset of AI that focuses on enabling machines to learn and improve from experience without being explicitly programmed.",
    "What is Deep Learning?": "Deep Learning is a subset of Machine Learning that uses neural networks with many layers to analyze data and make predictions.",
    "What is Natural Language Processing (NLP)?": "NLP is a field of AI that focuses on the interaction between computers and humans through natural language, enabling tasks like language translation and sentiment analysis.",
    "What is a Neural Network?": "A Neural Network is a series of algorithms designed to recognize patterns and mimic the operations of the human brain.",
    "What is Computer Vision?": "Computer Vision is a field of AI that enables machines to interpret and make decisions based on visual data such as images and videos.",
    "What is Reinforcement Learning?": "Reinforcement Learning is an area of Machine Learning where an agent learns to make decisions by performing actions and receiving rewards or penalties.",
    "What is a Chatbot?": "A Chatbot is an AI program designed to simulate conversation with users, often used for customer service or information retrieval.",
    "What is the Turing Test?": "The Turing Test is a method to determine whether a machine exhibits intelligent behavior indistinguishable from that of a human.",
    "What is the difference between AI and Machine Learning?": "AI is a broad concept of machines performing tasks intelligently, while Machine Learning is a subset of AI focused on enabling machines to learn from data.",
}

# Function to fetch Wikipedia summary using the wikipedia package
def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)  # Get first 2 sentences of the summary
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Sorry, the query is too broad. You may want to be more specific. Some options: {e.options[:5]}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "An error occurred while fetching information. Please try again."
    except wikipedia.exceptions.PageError:
        return f"Sorry, I couldn't find any relevant information on '{query}'."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Streamlit App
st.set_page_config(
    page_title="Student Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
with st.form("chat_input_form"):
    user_input = st.text_input("Ask a question:", placeholder="Type your question here...").strip()
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Split input into multiple questions if there are multiple queries
    questions = [q.strip() for q in user_input.split('and') if q.strip()]  # Split by 'and' or new lines

    for question in questions:
        # Display user's question
        st.session_state.history.append({"message": question, "is_user": True})

        # Check if question is predefined
        response = predefined_responses.get(question)
        
        # If not predefined, search Wikipedia dynamically
        if not response:
            response = get_wikipedia_summary(question)
        
        # Display chatbot's response
        st.session_state.history.append({"message": response, "is_user": False})

# Display chat history
for idx, chat in enumerate(st.session_state.history):
    message(chat["message"], is_user=chat["is_user"], key=f"message_{idx}")
