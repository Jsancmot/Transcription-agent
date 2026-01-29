"""
AI Transcription Agent with Groq and Tools
===========================================

This agent can transcribe audio files and manage a transcription
history using a Groq LLM and custom tools.

Author: Your Name
Project: Master in Generative AI - Deliverable
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from .tools.transcriber import TranscribeAudioTool
from .tools.history import (
    SaveTranscriptionTool,
    QueryHistoryTool
)


def load_configuration():
    """Loads environment variables from .env file"""
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "GROQ_API_KEY not configured.\n"
            "1. Copy .env.example to .env\n"
            "2. Get your free API key at: https://console.groq.com\n"
            "3. Add your API key to the .env file"
        )

    return api_key


def create_agent():
    """Creates and configures the transcription agent."""

    # Load API key
    api_key = load_configuration()

    # Initialize Groq LLM
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",  # Latest Llama model
        temperature=0.1,  # Low temperature for more precise responses
        max_tokens=4096
    )

    # Initialize tools
    tools = [
        TranscribeAudioTool(),
        SaveTranscriptionTool(),
        QueryHistoryTool()
    ]

    # Bind tools to LLM - the LLM will automatically decide which tool to use
    llm_with_tools = llm.bind_tools(tools)

    # Create intelligent agent using native function calling
    class IntelligentAgent:
        def __init__(self, llm_with_tools, tools):
            self.llm_with_tools = llm_with_tools
            self.tools = {tool.name: tool for tool in tools}

        def invoke(self, messages):
            """Process user message and execute appropriate tool."""
            try:
                user_message = messages["messages"][0]["content"]

                # LLM decides which tool to use based on tool descriptions
                response = self.llm_with_tools.invoke([
                    {"role": "system", "content": "Eres un asistente experto en transcripción de audio. Analiza el mensaje del usuario y usa la herramienta más apropiada según su intención."},
                    {"role": "user", "content": user_message}
                ])

                # Check if LLM wants to use a tool
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    tool_call = response.tool_calls[0]
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']

                    # Execute the selected tool
                    if tool_name in self.tools:
                        tool = self.tools[tool_name]
                        result = tool._run(**tool_args)
                        return {"messages": [{"content": str(result)}]}
                    else:
                        return {"messages": [{"content": f"Error: Herramienta {tool_name} no encontrada."}]}

                # If no tool call, return the LLM's direct response
                return {"messages": [{"content": response.content}]}

            except Exception as e:
                return {"messages": [{"content": f"Error al procesar tu solicitud: {str(e)}"}]}

    return IntelligentAgent(llm_with_tools, tools)


def main():
    """Main program function."""

    print("="*70)
    print("  AI TRANSCRIPTION AGENT")
    print("  Powered by Groq + Tools")
    print("="*70)
    print()

    try:
        # Create agent
        print("Initializing agent...")
        agent = create_agent()
        print("Agent ready!\n")

        # Startup information
        print("Available commands:")
        print("  - 'transcribe <file>' - Transcribe an audio file")
        print("  - 'history' - View previous transcriptions")
        print("  - 'search <term>' - Search in history")
        print("  - 'exit' - Close the program")
        print()

        # Main loop
        while True:
            try:
                # Request user input
                user_input = input("\n🎤 You: ").strip()

                if not user_input:
                    continue

                # Special commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nGoodbye!")
                    break

                # Execute agent
                print("\n🤖 Agent working...\n")
                result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

                # Show result
                print("\n" + "="*70)
                print("RESULT:")
                print("="*70)
                if 'messages' in result:
                    print(result['messages'][-1]['content'])
                else:
                    print(str(result))
                print("="*70)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Try again or type 'exit' to quit.")

    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
    except Exception as e:
        print(f"\n❌ Error initializing agent: {e}")
        print("\nMake sure you have installed the dependencies:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()