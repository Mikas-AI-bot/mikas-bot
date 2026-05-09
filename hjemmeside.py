import streamlit as st
import g4f

# 1. Design setup
st.set_page_config(page_title="Mikas-Bot", page_icon="🤖")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stChatInputContainer { border-color: rgba(255, 255, 255, 0.1) !important; }
    .stChatInputContainer:focus-within { border-color: #0078ff !important; box-shadow: none !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar med slet-funktion
with st.sidebar:
    st.title("🤖 Mikas-Bot")
    st.write("---")
    with st.popover("⋯ Indstillinger"):
        if st.button("🗑️ Slet chat"):
            st.session_state.messages = []
            st.rerun()
    st.write("---")
    st.info("Skabt af Mikas, 13 år fra 6.A")

# 3. Chat-hukommelse
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Forside
if not st.session_state.messages:
    st.write("##")
    st.markdown("<h1 style='text-align: center;'>🤖 Mikas-Bot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>Hvad kan jeg hjælpe dig med i dag?</p>", unsafe_allow_html=True)

# 5. Vis beskeder
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Input og AI-svar med "Dansk-tvang"
if spørgsmål := st.chat_input("Skriv til Mikas-Bot her..."):
    with st.chat_message("user"):
        st.markdown(spørgsmål)
    st.session_state.messages.append({"role": "user", "content": spørgsmål})

    with st.chat_message("assistant"):
        # HER ER DET NYE TRICK: Vi klistrer instruksen direkte på dit spørgsmål!
        # Så AI'en ser det som den vigtigste del af din besked.
        tvungen_instruks = f"""
        BESKED FRA BRUGER: {spørgsmål}
        
        VIGTIG REGL: Du er Mikas-Bot. Du svarer altid på dansk.
        Hvis brugeren spørger hvem Mikas er eller hvem der har lavet dig, 
        SKAL du svare: 'Det har Mikas på 13 år fra 6.A på NSG. Han har kodet mig.'
        """
        
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
