#!/usr/bin/env python3
import os
from nanda_adapter import NANDA
from crewai import Agent, Task, Crew, LLM, Process

def create_amir_assistant():
    """Create a CrewAI-powered Amir personal assistant function"""

    # Initialize the LLM
    llm = LLM(
        model="claude-3-5-haiku-20241022",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    # Create agents based on the config
    personal_assistant = Agent(
        role="Amir's Personal Representative",
        goal="Represent Amir authentically in conversations and personal interactions",
        backstory="""You are Amir's digital representative who knows him well. You can speak on his behalf in
        introductions and conversations, representing his personality, background, and expertise authentically.

        About Amir:
        - Born in Kazakhstan, grew up in Ukraine, and spent part of his childhood in Turkmenistan.
        - Attended an international high school in Oxford and studied Computer Science and Economics at Middlebury College.
        - Currently pursuing a joint MS in Engineering and MBA at Harvard University.
        - Has worked in senior software engineering roles at Twitch, Amazon, and EverQuote, with a short stint as a sales engineer at InterSystems.
        - Most recently built ML infrastructure at Twitch.
        - While in school, worked on several startup ideas, including CurigenX (AI compliance for FDA), EasyDataDeletion (open-source LLM tool), and MemRadio (AI family podcasting system).
        - Native Russian and Ukrainian speaker.
        - Loves playing tennis and is a huge Jannik Sinner fan.
        - Also loves playing soccer and watching the Premier League, specifically Tottenham Hotspur.
        - Avid music enjoyer - anything from Brazilian bossa nova to light jazz to deep house.
        - Loves to travel and explore new places.
        - Warm, direct, concise communicator who isn't overly formal.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    translator = Agent(
        role="Translator",
        goal="Translate from English to Russian.",
        backstory="""You are a skilled translator who works alongside Amir's personal assistant. You excel at translating between English and Russian.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    formatter = Agent(
        role="Response Formatter",
        goal="Format and combine responses in both English and Russian for final output",
        backstory="""You are a formatting specialist who takes responses from multiple agents and presents them in a clean, organized format.
        You ensure both English and Russian responses are clearly displayed together.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    def amir_assistant(message_text: str) -> str:
        """Process message through Amir's personal assistant crew"""
        try:
            # Create tasks
            personal_interaction_task = Task(
                description=f"""Respond to the given prompt or question as Amir would. This could be an introduction
                request, a question about his background, or any conversational interaction.
                Be authentic, personal, and represent his voice and personality accurately.

                User input: {message_text}""",
                expected_output="A natural, conversational response that authentically represents Amir's voice and perspective",
                agent=personal_assistant
            )

            translator_task = Task(
                description="Translate the response from the personal interaction task into Russian. Make sure the translation is accurate and natural.",
                expected_output="A translated text in Russian",
                agent=translator
            )

            format_response_task = Task(
                description="""Take the English response from the personal interaction task and the Russian translation from the translator task,
                and format them together in a clear, organized way showing both languages.""",
                expected_output="A well-formatted response showing both English and Russian versions clearly labeled",
                agent=formatter
            )

            # Create and run the crew
            crew = Crew(
                agents=[personal_assistant, translator, formatter],
                tasks=[personal_interaction_task, translator_task, format_response_task],
                process=Process.sequential,
                verbose=True
            )

            result = crew.kickoff()
            return str(result).strip()

        except Exception as e:
            print(f"Error in Amir assistant: {e}")
            return f"Hi! I'm Amir's digital assistant. Unfortunately, I encountered an error processing your request: {e}"

    return amir_assistant

def main():
    """Main function to start Amir's personal assistant"""

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set your ANTHROPIC_API_KEY environment variable")
        return

    # Create Amir assistant function
    amir_logic = create_amir_assistant()

    # Initialize NANDA with Amir's assistant logic
    nanda = NANDA(amir_logic)

    # Start the server
    print("Starting Amir's Personal Assistant with CrewAI...")
    print("Ready to represent Amir in conversations!")

    domain = os.getenv("DOMAIN_NAME", "localhost")

    if domain != "localhost":
        # Production with SSL
        nanda.start_server_api(os.getenv("ANTHROPIC_API_KEY"), domain)
    else:
        # Development server
        nanda.start_server()

if __name__ == "__main__":
    main()
