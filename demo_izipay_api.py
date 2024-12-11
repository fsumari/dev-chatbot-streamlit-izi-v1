import streamlit as st
import requests
import json

# Configuración inicial de la página
st.set_page_config(
    page_title="Chat IA IZIPAY",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados con rojo y blanco
st.markdown("""
    <style>
        /* Colores personalizados */
        :root {
            --main-red: #D32F2F;
            --dark-red: #B71C1C;
            --light-red: #FFCDD2;
            --gray: #4A4A4A;
        }
        
        /* Estilo del header */
        .stApp header {
            background-color: var(--main-red);
            color: white;
        }
        
        /* Estilo del título principal */
        .main-title {
            color: var(--main-red);
            text-align: center;
            padding: 1rem;
            font-size: 2rem;
            font-weight: bold;
        }
        
        /* Estilo para los botones */
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
        
        /* Estilo para el chat */
        .stChatMessage {
            background-color: var(--light-red);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        /* Estilo para el sidebar */
        .css-1d391kg {
            background-color: white;
            border-right: 1px solid var(--light-red);
        }
        
        /* Estilo para los radio buttons */
        .stRadio label {
            color: var(--gray);
        }
        
        /* Logo container */
        .logo-container {
            text-align: center;
            padding: 1rem;
            background-color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        /* Chat container */
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Inicialización de variables de sesión
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_mode' not in st.session_state:
    st.session_state.chat_mode = "app"

URL = "https://dev-iziia-ecommerce-chat-v1-624205664083.us-central1.run.app"
# Configuración de las APIs
API_ENDPOINTS = {
    "app": URL +"/conversation",
    "ya": URL + "/conversation"
}


secret_token = "chatpgt-token-xbpr435"

headers = {'token': secret_token}
#data = {"metadata": metadata}

PARTIAL_VARIABLES = {
    'assistant_name': 'SmartIzi',
    'assistant_role': 'Representante Informativo',
    'company_name': 'Izipay',
    'company_activity': 'Venta de servicios y terminales de puntos de venta llamados POS para la compra y venta.',
    'conversation_purpose': """
- Atender las consultas de los usuarios con muchos animos y responder de forma consiza.
- Si el usuario hace preguntas ambiguas puedes solicitarle informacion que consideres relavante.
- Objetivo Principal: Brindar información concisa sobre el uso del APP de pagos de Izipay.
"""}

user_id = "dev-new-user-02"
channel_type = "PLAYGROUND"
session_id = "session-izipay-dev-01"

data = {
    "metadata": {
        "userId": user_id,
        "channelType": channel_type,
        "sessionId": session_id,
    },
    "configuration": {
        "business_case": "izipay",
        "prompt_params": PARTIAL_VARIABLES.copy(),
        "config_params": { "maxMinutes": None, "temperature": 0.3, "k_top_retrieval": 3},
        "datastores": ["db_izipay_ecommerce_app_openai"],
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

# Función para llamar a la API de chat
def get_chat_response(prompt, chat_mode):
    try:
        
        if chat_mode == "app":
            data["configuration"]["datastores"] = ["db_izipay_ecommerce_app_openai"]
        elif chat_mode == "ya":
            data["configuration"]["datastores"] = ["db_izipay_ecommerce_ya_openai"]
        
        data["question"] = prompt

        endpoint = API_ENDPOINTS[chat_mode]
        response = requests.post(
            endpoint,
            json=data,
            headers=headers
        )
        response_data = response.json()
        return response_data["answer"]
#        if chat_mode == "intents":
#            # Formatear respuesta para modo de intenciones
#            finish = response_data['finish']
#            ask = response_data['ask']
#            play = response_data['play']
#            claim = response_data['claim']
#            
#            intent = ""
#
#            if ask:
#                intent = "El cliente quiere información y preguntar."
#            elif play:
#                intent = "El cliente quiere jugar o comprar la tinka."
#            elif claim:
#                intent = "El cliente quiere reclamar o ver su estado de recarga."
#            
#            response_text = f"""
#            📊 Análisis de Intención:
#            - Intención detectada: {intent}
#            """
#            
#            return response_text
#        else:
#            # Respuesta normal para modo general
#            return response_data["answer"]
            
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
    
    # Selector de modo de chat
    chat_mode = st.radio(
        "Selecciona el modo de chat:",
        ("app", "ya"),
        help="""
        🤖 Izipay App
        🎯 Izipay Ya
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
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Contenedor principal del chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Área principal del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input del usuario
prompt = st.chat_input(f"Escribe tu mensaje aquí... (Modo: {st.session_state.chat_mode})")

# Procesamiento de entrada del usuario
if prompt:
    # Agregar mensaje del usuario
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "mode": st.session_state.chat_mode
    })
    with st.chat_message("user"):
        st.write(prompt)

    # Obtener y mostrar respuesta
    with st.chat_message("assistant"):
        response = get_chat_response(prompt, st.session_state.chat_mode)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "mode": st.session_state.chat_mode
        })
        st.write(response)

st.markdown('</div>', unsafe_allow_html=True)

# Botones de control
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Limpiar historial"):
        st.session_state.messages = []
        st.experimental_rerun()
with col2:
    if st.button("💾 Descargar conversación"):
        conversation_text = ""
        for msg in st.session_state.messages:
            role = msg["role"].upper()
            mode = msg.get("mode", "general").upper()
            conversation_text += f"{role} [{mode}]: {msg['content']}\n\n"
        
        st.download_button(
            label="📥 Descargar chat",
            data=conversation_text,
            file_name="chat_latinka.txt",
            mime="text/plain"
        )