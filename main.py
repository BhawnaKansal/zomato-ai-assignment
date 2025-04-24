
import argparse
import gradio as gr
from knowledge_base import KnowledgeBase
from rag_chatbot import SimpleRAGChatbot
from typing import List, Tuple

def gradio_interface(query: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    response = chatbot.handle_query(query)
    history.append((query, response))
    return "", history

def main(args):
    global chatbot
    kb = KnowledgeBase(args.input)
    chatbot = SimpleRAGChatbot(kb)

    with gr.Blocks() as demo:
        gr.Markdown("""
        # Swiggy Restaurant Chatbot (Hugging Face RAG)
        Ask about restaurant menus, vegan options, price ranges, or compare spice levels. Examples:
        - "What vegan dishes are available?"
        - "What is the spice level of egg bhurji at Desi Tadka?"
        - "Which restaurants serve Italian?"
        """)
        chatbot_ui = gr.Chatbot(label="Conversation")
        query_input = gr.Textbox(label="Your Query", placeholder="Type your question here...")
        submit_button = gr.Button("Submit")
        submit_button.click(
            fn=gradio_interface,
            inputs=[query_input, chatbot_ui],
            outputs=[query_input, chatbot_ui]
        )

    demo.launch(share=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a RAG-based chatbot for Swiggy restaurant data using Hugging Face.')
    parser.add_argument('--input', type=str, default='swiggy_data.json', help='Path to input JSON file')
    args = parser.parse_args()
    main(args)
