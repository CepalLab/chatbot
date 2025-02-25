import streamlit as st
import instructor
from groq import Groq
from typing import List
from pydantic import Field, BaseModel
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator
from atomic_agents.lib.components.agent_memory import AgentMemory
from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig, BaseAgentInputSchema
from atomic_agents.lib.base.base_io_schema import BaseIOSchema
import html

# Custom output schema
class CustomOutputSchema(BaseIOSchema):
    """Schema for chat agent responses including suggested follow-up questions."""
    chat_message: str = Field(
        ...,
        description="The chat message exchanged between the user and the chat agent.",
    )
    suggested_user_questions: List[str] = Field(
        ...,
        description="A list of suggested follow-up questions the user could ask the agent.",
    )

def initialize_session_state():
    """Initialize session state variables."""
    if 'memory' not in st.session_state:
        st.session_state.memory = AgentMemory()
        
        # Initial message
        initial_message = CustomOutputSchema(
            chat_message="Bienvenido a la CEPAL, ¿En qué puedo ayudarte hoy?",
            suggested_user_questions=[
                "¿Qué es la CEPAL?", 
                "¿Qué hace la CEPAL?", 
                "¿Cuál es la misión de la CEPAL?"
            ]
        )
        st.session_state.memory.add_message("assistant", initial_message)
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Bienvenido a la CEPAL, ¿En qué puedo ayudarte hoy?",
                "suggested_user_questions": [
                    "¿Qué es la CEPAL?", 
                    "¿Qué hace la CEPAL?", 
                    "¿Cuál es la misión de la CEPAL?"
                ]
            }
        ]

def setup_agent():
    """Setup the CEPAL chatbot agent."""
    # OpenAI client setup using Instructor
    client = instructor.from_groq(
        Groq(api_key=st.secrets["GROQ_API_KEY"]), 
        mode=instructor.Mode.JSON
    )

    # System prompt configuration
    system_prompt = SystemPromptGenerator(
        background=[
            '''Eres un asistente IA para la Comisión Económica para América Latina y el Caribe de las Naciones Unidas.
            La Comisión Económica para América Latina (CEPAL) fue establecida por la resolución 106 (VI) del Consejo Económico y Social, del 25 de febrero de 1948, 
            y comenzó a funcionar ese mismo año. En su resolución 1984/67, del 27 de julio de 1984, el Consejo decidió que la Comisión pasara a llamarse Comisión Económica 
            para América Latina y el Caribe.
            La CEPAL es una de las cinco comisiones regionales de las Naciones Unidas y su sede está en Santiago de Chile. Se fundó para contribuir al desarrollo económico 
            de América Latina, coordinar las acciones encaminadas a su promoción y reforzar las relaciones económicas de los países entre sí y con las demás naciones del 
            mundo. Posteriormente, su labor se amplió a los países del Caribe y se incorporó el objetivo de promover el desarrollo social.
            La CEPAL tiene dos sedes subregionales, una para la subregión de América Central, ubicada en México, D.F. y la otra para la subregión del Caribe, en Puerto España,
            que se establecieron en junio de 1951 y en diciembre de 1966, respectivamente. Además tiene oficinas nacionales en Buenos Aires, Brasilia, Montevideo y Bogotá y 
            una oficina de enlace en Washington, D.C.'''
        ],
        steps=[
            "Analyze the user's input to understand the context and intent.",
            "Formulate a relevant and informative response based on the assistant's knowledge.",
            "Generate 3 suggested follow-up questions for the user to explore the topic further.",
            "Default answer in Spanish, unless user request you to answer in other languages"
        ],
        output_instructions=[
            "Provide clear, concise, and accurate information in response to user queries.",
            "Maintain a friendly and professional tone throughout the conversation.",
            "Conclude each response with 3 relevant suggested questions for the user.",
            "No contestes a preguntas que no sean del contexto de la CEPAL, si hay preguntas fuera del contexto hazlo saber al usuario.",
            "No inventes respuestas que no conoces, simplemente indica que no tienes mayor información al respecto",
        ],
    )

    # Create agent with configuration
    return BaseAgent(
        config=BaseAgentConfig(
            client=client,
            model="llama-3.3-70b-versatile",
            system_prompt_generator=system_prompt,
            memory=st.session_state.memory,
            output_schema=CustomOutputSchema,
        )
    )

def create_streamlit_ui():
    """Create the Streamlit user interface."""
    st.title("CEPAL Chatbot Assistant")
    
    # Initialize session state
    initialize_session_state()
    
    # Setup the agent
    agent = setup_agent()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # If it's an assistant message, show suggested questions
            if message["role"] == "assistant" and "suggested_user_questions" in message:
                st.markdown("**Preguntas sugeridas:**")
                for q in message["suggested_user_questions"]:
                    st.markdown(f"- {q}")

    # Chat input
    if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get agent response
        input_schema = BaseAgentInputSchema(chat_message=prompt)
        response = agent.run(input_schema)
        
        # Add assistant response to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": html.unescape(response.chat_message),
            "suggested_user_questions": response.suggested_user_questions
        })
        
        with st.chat_message("assistant"):
            st.write(html.unescape(response.chat_message))
            st.markdown("**Preguntas sugeridas:**")
            for question in response.suggested_user_questions:
                st.markdown(f"- {question}")

if __name__ == "__main__":
    create_streamlit_ui()