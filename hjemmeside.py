import streamlit as st
import g4f

# 1. Design setup - Tvinger side-menuen til at være åben (expanded)
st.set_page_config(
    page_title="Mikas-Bot", 
    page_icon="🤖", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Skjuler Streamlit menuer og deploy knapper */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fjerner rød kant på skrivefeltet */
    .stChatInputContainer { border-color: rgba(255, 255, 255, 0.1) !important; }
    .stChatInputContainer:focus-within { border-color: #0078ff !important; box-shadow: none !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Venstre side-menu (Sidebar)
with st.sidebar:
    st.title("🤖 Mikas-Bot")
    st.write("---")
    # Menu med de tre prikker til at slette chatten
    with st.popover("⋯ Indstillinger"):
        if st.button("🗑️ Slet chat"):
            st.session_state.messages = []
            st.rerun()
    st.write("---")
    st.info("Skabt af Mikas, 13 år fra 6.A")

# 3. Chat-hukommelse
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. FORSIDE (Logo i midten når chatten er tom)
if not st.session_state.messages:
    st.write("##")
    st.write("##")
    st.markdown("<h1 style='text-align: center;'>🤖 Mikas-Bot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>Hvad kan jeg hjælpe dig med i dag?</p>", unsafe_allow_html=True)

# 5. Vis beskeder
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Skrivefelt og AI-svar
if spørgsmål := st.chat_input("Skriv til Mikas-Bot her..."):
    with st.chat_message("user"):
        st.markdown(spørgsmål)
    st.session_state.messages.append({"role": "user", "content": spørgsmål})

    with st.chat_message("assistant"):
        # Her er instruksen der beviser det er dig!
        tvungen_instruks = f"BRUGER SPØRGER: {spørgsmål}. REGLER: Du er Mikas-Bot skabt af Mikas på 13 år fra 6.A på NSG. Svar altid på dansk."
        
        try:
            respons = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": tvungen_instruks}],
            )
            st.markdown(respons)
        except:
            respons = "Hov, jeg har lidt svært ved at forbinde. Prøv at slette chatten!"
            st.markdown(respons)
            
    st.session_state.messages.append({"role": "assistant", "content": respons})
    st.rerun()
