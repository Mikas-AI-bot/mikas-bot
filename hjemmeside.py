import streamlit as st
import g4f

# 1. Design setup - fjerner rod og sikrer at side-menuen kan findes
st.set_page_config(page_title="Mikas-Bot", page_icon="🤖")

st.markdown("""
    <style>
    /* Skjuler Streamlit menuer og deploy knapper */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fjerner rød kant på skrivefeltet */
    .stChatInputContainer { border-color: rgba(255, 255, 255, 0.1) !important; }
    .stChatInputContainer:focus-within { border-color: #0078ff !important; box-shadow: none !important; }
    
    /* Gør den lille pil til side-menuen mere synlig hvis den er lukket */
    .st-emotion-cache-6q9sum.ef3ps4x0 {
        background-color: #0078ff !important;
        color: white !important;
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Venstre side-menu (Sidebar)
with st.sidebar:
    st.title("🤖 Mikas-Bot")
    st.write("---")
    # Menuen med de tre prikker
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
        # DIN PERSONLIGE SIGNATUR OG INSTRUKSER:
        instruks = """
        Du er Mikas-Bot. Du svarer altid på DANSK.
        Hvis folk spørger hvem der har lavet dig, svarer du: 'Det har Mikas på 13 år. Han går i 6.A på NSG.'
        Hvis folk spørger hvem Mikas er, svarer du: 'Mikas er ham, der har kodet og programmeret mig.'
        """
        
        try:
            respons = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": instruks},
                    {"role": "user", "content": spørgsmål}
                ],
            )
            st.markdown(respons)
        except:
            respons = "Hov, jeg mistede forbindelsen. Prøv at slette chatten i menuen til venstre!"
            st.markdown(respons)
            
    st.session_state.messages.append({"role": "assistant", "content": respons})
    st.rerun()
