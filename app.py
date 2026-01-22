import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
import json
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(
    page_title="Nexus AI Assistant",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS Premium Amélioré
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 100%);
        color: #ffffff;
    }
    
    /* Titre avec effet de lueur amélioré */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #0080ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.5));
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #8b949e;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar stylisée */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1535 0%, #1a2555 100%);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(0, 212, 255, 0.3);
        box-shadow: -10px 0 30px rgba(0, 212, 255, 0.1);
    }
    
    /* Bulles de chat améliorées */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.05);
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 212, 255, 0.3) !important;
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.15) !important;
    }
    
    /* Boutons améliorés */
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff 0%, #0080ff 100%);
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
        font-size: 0.95rem !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.5);
    }
    
    /* Cartes de modèles */
    .model-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 128, 255, 0.05) 100%);
        padding: 18px;
        border-radius: 15px;
        border-left: 4px solid #00d4ff;
        border: 1px solid rgba(0, 212, 255, 0.2);
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .model-card:hover {
        border-color: rgba(0, 212, 255, 0.4);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.2);
    }
    
    .model-desc {
        font-size: 0.9rem;
        color: #b0b0c0;
        line-height: 1.5;
        margin-top: 8px;
    }
    
    /* Chat input */
    .stChatInputContainer {
        border-top: 1px solid rgba(0, 212, 255, 0.2);
        padding-top: 1rem;
    }
    
    /* Masquer les éléments inutiles */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider */
    hr {
        border-color: rgba(0, 212, 255, 0.2) !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: rgba(0, 212, 255, 0.05) !important;
        border-left: 4px solid #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuration des modèles
MODELS_CONFIG = {
    "Molmo 2 8B": {
        "id": "allenai/molmo-2-8b:free",
        "desc": "🎨 L'expert en vision. Capable d'analyser, décrire et comprendre vos images avec une précision chirurgicale.",
        "vision": True
    },
    "GPT-OSS-120B": {
        "id": "deepseek/deepseek-chat",
        "desc": "🧠 Le titan du texte. Un modèle massif de 120B+ paramètres, exceptionnel pour la génération de contenu complexe.",
        "vision": False
    }
}

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def save_conversation(messages, model_name):
    """Sauvegarde une conversation dans le fichier JSON"""
    conversations_file = "conversations.json"
    
    conversations = []
    if os.path.exists(conversations_file):
        with open(conversations_file, "r", encoding="utf-8") as f:
            conversations = json.load(f)
    
    conversation = {
        "id": len(conversations) + 1,
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    conversations.append(conversation)
    
    with open(conversations_file, "w", encoding="utf-8") as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)
    
    return conversation["id"]

def load_conversations():
    """Charge toutes les conversations"""
    conversations_file = "conversations.json"
    if os.path.exists(conversations_file):
        with open(conversations_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def export_conversation_markdown(messages, model_name):
    """Exporte une conversation en Markdown"""
    md_content = f"# Conversation Nexus AI Assistant\n\n"
    md_content += f"**Modèle utilisé:** {model_name}\n"
    md_content += f"**Date:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    md_content += "---\n\n"
    
    for msg in messages:
        role = "👤 Vous" if msg["role"] == "user" else "🤖 Nexus AI"
        md_content += f"## {role}\n\n{msg['content']}\n\n---\n\n"
    
    return md_content

# Initialisation de l'état de session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_model" not in st.session_state:
    st.session_state.current_model = "Molmo 2 8B"
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# Barre latérale
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00d4ff; font-size: 1.8rem;'>🌌 Nexus Control</h2>", unsafe_allow_html=True)
    st.divider()
    
    # Onglets pour la navigation
    tab1, tab2 = st.tabs(["💬 Chat", "📚 Historique"])
    
    with tab1:
        # Sélection du modèle avec détection de changement
        new_model = st.selectbox(
            "🤖 Intelligence Artificielle",
            options=list(MODELS_CONFIG.keys()),
            index=list(MODELS_CONFIG.keys()).index(st.session_state.current_model)
        )
        
        # Logique de réinitialisation au changement de modèle
        if new_model != st.session_state.current_model:
            st.session_state.current_model = new_model
            st.session_state.messages = []
            st.rerun()
        
        model_info = MODELS_CONFIG[st.session_state.current_model]
        
        # Carte descriptive du modèle
        st.markdown(f"""
            <div class='model-card'>
                <div style='font-weight: 700; color: #00d4ff; margin-bottom: 8px; font-size: 1.1rem;'>{st.session_state.current_model}</div>
                <div class='model-desc'>{model_info['desc']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Affichage conditionnel de l'upload d'image
        uploaded_file = None
        if model_info["vision"]:
            st.markdown("### 📸 Vision")
            uploaded_file = st.file_uploader("Analyser une image", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Image chargée", use_container_width=True)
        else:
            st.info("💡 GPT-OSS-120B est un expert textuel pur. Utilisez Molmo 2 8B pour l'analyse d'images.")
        
        st.divider()
        
        # Boutons d'action
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Sauvegarder", use_container_width=True):
                if st.session_state.messages:
                    save_conversation(st.session_state.messages, st.session_state.current_model)
                    st.success("✅ Conversation sauvegardée!")
                else:
                    st.warning("⚠️ Aucun message à sauvegarder")
        
        with col2:
            if st.button("🗑️ Réinitialiser", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    with tab2:
        st.markdown("### 📚 Historique des Conversations")
        conversations = load_conversations()
        
        if conversations:
            for conv in reversed(conversations):
                with st.expander(f"🕐 {conv['timestamp'][:10]} - {conv['model']}"):
                    st.write(f"**Modèle:** {conv['model']}")
                    st.write(f"**Messages:** {len(conv['messages'])}")
                    
                    # Aperçu des messages
                    for msg in conv['messages'][:3]:
                        role = "👤" if msg['role'] == 'user' else "🤖"
                        preview = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                        st.caption(f"{role} {preview}")
                    
                    # Bouton d'export
                    md_content = export_conversation_markdown(conv['messages'], conv['model'])
                    st.download_button(
                        label="📥 Exporter en Markdown",
                        data=md_content,
                        file_name=f"nexus_conversation_{conv['id']}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
        else:
            st.info("📭 Aucune conversation sauvegardée pour le moment")

# Récupération de la clé API
api_key = st.secrets.get("OPENROUTER_API_KEY")

if not api_key:
    st.error("❌ Configuration manquante : OPENROUTER_API_KEY")
    st.stop()

# Initialisation du client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Interface principale
st.markdown("<h1 class='main-title'>🌌 Nexus AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>L'intelligence artificielle, redéfinie.</p>", unsafe_allow_html=True)

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Transmettez votre commande..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        model_info = MODELS_CONFIG[st.session_state.current_model]
        
        # Préparation du contenu (Multimodal ou Texte seul)
        if model_info["vision"] and uploaded_file:
            content = [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encode_image(image)}"}
                }
            ]
        else:
            content = prompt

        try:
            response = client.chat.completions.create(
                model=model_info["id"],
                messages=[{"role": "user", "content": content}],
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"❌ Nexus a rencontré une anomalie : {e}")

st.markdown("---")
st.caption("🌌 Nexus AI Framework v3.0 | Sécurisé & Optimisé | Amélioré par Manus")
