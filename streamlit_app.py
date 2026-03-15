import streamlit as st
from openai import OpenAI
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO

st.set_page_config(
    page_title="AI Study Notes Generator",
    page_icon="📘",
    layout="wide",
)

api_key = st.secrets.get("OPENAI_API_KEY") if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ API key not found. Please set OPENAI_API_KEY in Streamlit secrets.")
    st.stop()

client = OpenAI(
    
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def generate_pdf(title, content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1E3A8A',
        spaceAfter=0.3*inch,
        alignment=1
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        spaceAfter=0.1*inch
    )
    
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    content_paragraphs = content.split('\n')
    for para in content_paragraphs:
        if para.strip():
            elements.append(Paragraph(para.strip(), body_style))
        else:
            elements.append(Spacer(1, 0.1*inch))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🧠 Generate Notes", "ℹ️ About Project"])

if page == "🏠 Home":
    st.title("📘 AI Study Notes Generator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        Welcome to **AI Study Notes Generator**, your smart study buddy built for students! 🎓

        This web app helps you instantly generate short, clear, and easy-to-understand notes on any topic using **AI**.

        ### 💡 Key Features:
        - ✨ **Smart Note Generation** – Create focused study notes instantly
        - 🎯 **Difficulty Levels** – Choose Beginner, Intermediate, or Advanced
        - 📥 **Easy Downloads** – Export notes for offline study
        - ⚡ **Lightning Fast** – AI-powered generation in seconds
        - 🎨 **Clean Interface** – Built for students, by students

        ---
        **Ready to get started?** Click on the **'🧠 Generate Notes'** tab in the sidebar!
        """)
    
    with col2:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/3233/3233495.png",
            caption="Your AI Study Partner 🤖",
            width=280
        )

elif page == "🧠 Generate Notes":
    st.title("🧠 Generate Study Notes with AI")
    st.write("📝 Enter any topic and choose your difficulty level to get started!")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_input(
            "📖 Enter the topic:",
            placeholder="e.g., Photosynthesis, World War II, Calculus...",
            help="Be specific for better results"
        )
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty Level:",
            ["Beginner", "Intermediate", "Advanced"],
            help="Choose the level of detail and complexity"
        )
    
   
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        generate = st.button("✨ Generate", use_container_width=True)
    
    with col_btn2:
        clear = st.button("🔄 Clear", use_container_width=True)
    
    if clear:
        st.rerun()

    if generate:
        if not topic or topic.strip() == "":
            st.error("⚠️ Please enter a topic first.")
        elif len(topic.strip()) < 2:
            st.error("⚠️ Topic must be at least 2 characters long.")
        else:
            with st.spinner("🤖 Generating your study notes... please wait..."):
                try:
                    
                    difficulty_config = {
                        "Beginner": {"notes": 3, "detail": "simple and concise", "max_tokens": 300},
                        "Intermediate": {"notes": 5, "detail": "moderately detailed", "max_tokens": 500},
                        "Advanced": {"notes": 7, "detail": "comprehensive and detailed", "max_tokens": 700},
                    }
                    
                    config = difficulty_config[difficulty]
                    prompt = f"Create {config['notes']} {config['detail']} bullet-point study notes about {topic}. Make them educational, well-organized, and easy to understand for students."

                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful study assistant that creates clear, well-organized study notes for students."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=config["max_tokens"],
                        temperature=0.7,
                    )

                    notes = response.choices[0].message.content.strip()

                    
                    st.divider()
                    st.subheader(f"📄 Study Notes: {topic.title()}")
                    st.info(f"📚 Difficulty: **{difficulty}** | 🤖 AI Generated | ⏱️ Optimized for learning")
                    st.markdown(notes)
                    st.divider()
                    
                    st.success("✅ Notes generated successfully!")

                    pdf_data = generate_pdf(f"Study Notes: {topic.title()}", notes)
                    st.download_button(
                        label="⬇️ Download as PDF",
                        data=pdf_data,
                        file_name=f"{topic.replace(' ', '_')}_notes_{difficulty.lower()}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"❌ Error generating notes: {str(e)}")
                    st.info("💡 Tip: Make sure your API key is valid and you have an active internet connection.")

elif page == "ℹ️ About Project":
    st.title("ℹ️ About This Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📘 Project Overview")
        st.write("""
        **AI Study Notes Generator** was created during a **college hackathon** to solve a real problem: students spend too much time taking notes instead of learning.
        
        Our mission is to use AI to help students **study smarter, not harder** by generating high-quality, focused study notes instantly.
        """)
    
    with col2:
        st.subheader("🧩 Technologies Used")
        st.markdown("""
        - **Python** – Core logic & backend
        - **Streamlit** – Interactive web interface
        - **OpenAI API** – AI content generation
        - **OpenRouter** – API optimization
        """)
    
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("👩‍💻 Team Members")
        st.markdown("""
        - 🎨 **Bharadwaj** – Frontend & Design (HTML, CSS)
        - ⚙️ **Backend Developer** – Python & AI Integration
        """)
    
    with col4:
        st.subheader("🚀 Planned Features")
        st.markdown("""
        - 🔊 Text-to-speech for notes
        - ❓ Auto-generated quiz questions
        - 📊 Progress tracking
        - 💾 Save & organize notes
        - 📚 Subject-specific templates
        """)
    
    st.divider()
    st.info("💡 **Pro Tips:**\n- Be specific with topics (e.g., 'Photosynthesis light reactions' instead of just 'photosynthesis')\n- Use higher difficulty levels for deeper understanding\n- Save your notes for future reference!")
    st.write("---")
    st.caption("✨ Made with ❤️ using Python, Streamlit, and AI")