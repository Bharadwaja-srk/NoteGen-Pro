
import streamlit as st
import openrouter
 
openrouter.api_key = "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"
 
st.set_page_config(
     page_title="AI Study Notes Generator",
     page_icon="📘",
     layout="centered",
 )
 
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🧠 Generate Notes", "ℹ️ About Project"])
 
if page == "🏠 Home":
     st.title("📘 AI Study Notes Generator")
     st.write("""
     Welcome to **AI Study Notes Generator**, your smart study buddy built for students! 🎓  
     This web app helps you instantly generate short, clear, and easy-to-understand notes on any topic using **AI**.
     
     ### 💡 Features:
     - Generate short study notes for any topic  
    - Built using **Python + Streamlit + OpenRouter API**  
     - Download notes easily for offline use  
     - Simple, fast, and student-friendly  
 
     ---
     Click on the **'🧠 Generate Notes'** page in the sidebar to start!
     """)
     st.image(
         "https://cdn-icons-png.flaticon.com/512/3233/3233495.png",
         caption="Your AI Study Partner 🤖",
         width=200
     )
 
elif page == "🧠 Generate Notes":
     st.title("🧠 Generate Study Notes with AI")
     st.write("Enter any topic below and let AI help you study smarter!")
 
     topic = st.text_input("Enter the topic:")
     generate = st.button("✨ Generate Notes")
 
     if generate:
         if topic.strip() == "":
             st.warning("⚠️ Please enter a topic first.")
         else:
             with st.spinner("🤖 Generating your study notes... please wait..."):
                 try:
                     response = openrouter.Completion.create(
                         model="text-davinci-003",
                         prompt=f"Write 5 short and simple bullet-point study notes about {topic}.",
                         max_tokens=150,
                         temperature=0.7
                     )
                     notes = response.choices[0].text.strip()
 
                     st.subheader(f"📄 Study Notes on {topic.title()}:")
                     st.write(notes)
                     st.success("✅ Notes generated successfully!")
 
                     st.download_button(
                         label="⬇️ Download Notes",
                         data=notes,
                         file_name=f"{topic}_notes.txt",
                         mime="text/plain"
                     )
 
                 except Exception as e:
                     st.error(f"❌ Error: {e}")
 
elif page == "ℹ️ About Project":
     st.title("ℹ️ About This Project")
     st.write("""
     ### 📘 AI Study Notes Generator
     This project was developed as part of a **college hackathon**.  
     The main goal is to make studying faster and smarter using **Artificial Intelligence**.
 
     ### 🧩 Technologies Used:
     - **Python** for logic and backend  
     - **Streamlit** for creating the web interface  
    - **OpenRouter API** for AI-powered content generation  
 
     ### 👩‍💻 Team Members:
     - Frontend Designer: *Bharadwaj* (HTML & CSS)
     - Backend Developer: *Your Friend* (Python & AI Integration)
 
     ### 🚀 Future Upgrades:
     - Add text-to-speech for reading notes aloud  
     - Add quiz generation from the same topic  
     - Support multiple subjects and difficulty levels  
 
     ---
     **Made with ❤️ using Python, Streamlit, and AI**
     """)
 