import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="Chat IA IZIPAY",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados con rojo y blanco (manteniendo los estilos existentes)
st.markdown("""
    <style>
        /* Colores personalizados */
        :root {
            --main-red: #D32F2F;
            --dark-red: #B71C1C;
            --light-red: #FFCDD2;
            --gray: #4A4A4A;
        }
        
        /* Manteniendo todos los estilos anteriores... */
        .stApp header {
            background-color: var(--main-red);
            color: white;
        }
        
        .main-title {
            color: var(--main-red);
            text-align: center;
            padding: 1rem;
            font-size: 2rem;
            font-weight: bold;
        }
        
        .stButton button {
            background-color: var(--main-red);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 0.5rem 1rem;
        }
        
        .stButton button:hover {
            background-color: var(--dark-red);
        }
        
        .stChatMessage {
            background-color: var(--light-red);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .css-1d391kg {
            background-color: white;
            border-right: 1px solid var(--light-red);
        }
        
        .stRadio label {
            color: var(--gray);
        }
        
        .logo-container {
            text-align: center;
            padding: 1rem;
            background-color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Nuevo estilo para el botón de reinicio de sesión */
        .reset-session-button {
            margin-top: 1rem;
            padding: 0.5rem;
            background-color: var(--main-red);
            color: white;
            border-radius: 5px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Función para generar un nuevo session_id
def generate_session_id():
    return f"dev-test-streamlit-{str(uuid.uuid4())}"

# Inicialización de variables de sesión
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_mode' not in st.session_state:
    st.session_state.chat_mode = "app"
if 'session_id' not in st.session_state:
    st.session_state.session_id = generate_session_id()

# URLs y configuración de API (manteniendo las existentes)
URL_APP_YA = "https://dev-chat-izipay-api-genai-iapp-iya-v1-624205664083.us-central1.run.app"
URL_SOTE = "https://dev-chat-izipay-api-genai-sote-v1-624205664083.us-central1.run.app"
URL_REIN_AGIZ = "https://dev-chat-izipay-api-genai-rein-agiz-v1-624205664083.us-central1.run.app"

API_ENDPOINTS = {
    "App": URL_APP_YA + "/conversation",
    "Ya": URL_APP_YA + "/conversation",
    "Soporte": URL_SOTE + "/conversation",
    "Agente Izipay": URL_REIN_AGIZ + "/conversation",
    "Retiro Inmediato": URL_REIN_AGIZ + "/conversation",
}

secret_token = "dev-chatpgt-token-xbpr435"
headers = {'token': secret_token}

PARTIAL_VARIABLES = {
    'assistant_name': 'SmartIzi',
    'assistant_role': 'Representante Informativo',
    'company_name': 'Izipay',
    'company_activity': 'Venta de servicios y terminales de puntos de venta llamados POS para la compra y venta.',
    'conversation_purpose': """
- Atender las consultas de los usuarios con muchos animos y responder de forma consiza.
- Si el usuario inicia la conversación con un Hola o saluda, indicale que resolveras sus preguntas acerca de soporte de izipay.
- Si el usuario hace preguntas ambiguas puedes solicitarle informacion que consideres relavante.
- Objetivo Principal: Brindar información concisa sobre soporte de todos los productos de Izipay.
"""
}

user_id = "dev-test-streamlit-user-general"
channel_type = "PLAYGROUND"

# Función para reiniciar la sesión
def reset_session():
    st.session_state.session_id = generate_session_id()
    st.session_state.messages = []
    st.rerun()

# Actualizar la configuración de data para usar el session_id dinámico
data = {
    "metadata": {
        "userId": user_id,
        "channelType": channel_type,
        "sessionId": st.session_state.session_id,
    },
    "configuration": {
        "business_case": "izipay",
        "prompt_params": PARTIAL_VARIABLES.copy(),
        "config_params": {"maxMinutes": None, "temperature": 0.3, "k_top_retrieval": 3},
    }
}

# Logo de Izipay
st.markdown("""
    <div class="logo-container">
        <img src="https://checkandtoc.com/wp-content/uploads/2020/07/Izipaylogo.png" 
             alt="Logo Izipay" 
             style="height: 80px; margin: auto;">
    </div>
""", unsafe_allow_html=True)

# Función get_chat_response (manteniendo la existente)
def get_chat_response(prompt, chat_mode):
    try:
        if chat_mode == "App":
            data["configuration"]["knowledge_stores"] = ["db_izipay_ecommerce_app_openai_dev"]
            data["configuration"]["typification_stores"] = ["db_izipay_tipificaciones_app_openai_dev"]
        elif chat_mode == "Ya":
            data["configuration"]["knowledge_stores"] = ["db_izipay_ecommerce_ya_openai_dev"]
            data["configuration"]["typification_stores"] = ["db_izipay_tipificaciones_ya_openai_dev"]
        elif chat_mode == "Soporte":
            data["configuration"]["knowledge_stores"] = ["db_izipay_ecommerce_sote_openai_dev"]
            data["configuration"]["typification_stores"] = ["db_izipay_tipificaciones_sote_openai_dev"]
        elif chat_mode == "Agente Izipay":
            data["configuration"]["knowledge_stores"] = ["dev_izipay_index_agiz_azureopenai"]
        elif chat_mode == "Retiro Inmediato":
            data["configuration"]["knowledge_stores"] = ["dev_izipay_index_rein_azureopenai"]
        
        # Actualizar el session_id en cada llamada
        data["metadata"]["sessionId"] = st.session_state.session_id
        data["question"] = prompt

        endpoint = API_ENDPOINTS[chat_mode]
        response = requests.post(
            endpoint,
            json=data,
            headers=headers
        )

        return response.json()
            
    except Exception as e:
        return f"Error al procesar la pregunta: {str(e)}"

# Título de la aplicación
st.title("Chat IA Izipay 🤖")

# Sidebar con configuración
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: var(--main-red);">💬 Configuración del Chat</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Mostrar el ID de sesión actual
    st.markdown(f"**ID de Sesión Actual:** `{st.session_state.session_id}`")
    
    # Botón para reiniciar sesión
    if st.button("🔄 Reiniciar Sesión"):
        reset_session()
    
    # Selector de modo de chat
    chat_mode = st.radio(
        "Selecciona el modo de chat:",
        ("App", "Ya", "Soporte", "Agente Izipay", "Retiro Inmediato"),
        help="""
        🤖 Izipay App
        🎯 Izipay Ya
        📊 Soporte
        🤖 Agenete Izipay
        📊 Retiro Inmediato
        """,
        key="chat_mode_selector"
    )
    st.session_state.chat_mode = chat_mode
    
    st.markdown("""
        <div style="background-color: white; padding: 1rem; border-radius: 10px; margin-top: 2rem; border: 1px solid var(--light-red);">
            <h3 style="color: var(--main-red);">Funcionalidades disponibles:</h3>
            <ul style="color: var(--gray);">
                <li>💭 Chat para consultas</li>
                <li>📝 Historial de conversación</li>
                <li>🔄 Reinicio de sesión</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Resto del código de chat (manteniendo el existente)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input(f"Escribe tu mensaje aquí... (Modo: {st.session_state.chat_mode})")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "mode": st.session_state.chat_mode
    })
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = get_chat_response(prompt, st.session_state.chat_mode)
        response_text = response["answer"]
        trace = response["trace"]
        trace_description = response["trace_description"]
        citations = response["citations"]

        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "mode": st.session_state.chat_mode
        })
        st.write(response_text)
        with st.expander("Referencias"):
            st.write("Traza: ", trace)
            st.write("Descripción de Traza: ", trace_description)
            if isinstance(citations, list):
                for count, ref in enumerate(citations):
                    st.write(f"[{count + 1}]", ref["page_content"])
                    st.write("Metadata: ", ref["metadata"])

st.markdown('</div>', unsafe_allow_html=True)

# Botones de control
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🗑️ Limpiar historial"):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("🔄 Nueva Sesión"):
        reset_session()
with col3:
    if st.button("💾 Descargar conversación"):
        conversation_text = f"ID de Sesión: {st.session_state.session_id}\n\n"
        for msg in st.session_state.messages:
            role = msg["role"].upper()
            mode = msg.get("mode", "general").upper()
            conversation_text += f"{role} [{mode}]: {msg['content']}\n\n"
        
        st.download_button(
            label="📥 Descargar chat",
            data=conversation_text,
            file_name=f"chat_izipay_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )