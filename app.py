import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps # This is for the image to be automatically-cropping
import os

# FOR PDF GENERATION FUNCTION
def create_pdf(name, email, linkedin, role, experience_list, education, skills_list, accent_color, profile_pic):
    pdf = FPDF()
    pdf.add_page()
    
    # Convert hex color to RGB
    hex_color = accent_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # HEADER SECTION
    pdf.set_fill_color(r, g, b)
    pdf.rect(0, 0, 210, 50, 'F') 
    
    text_x_offset = 10
    if profile_pic:
        # IMAGE auto-cropping into 1:1
        img = Image.open(profile_pic)
        
        # Center crop for it to make it a perfect 1:1 square
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        img = img.crop((left, top, right, bottom))
        
        temp_path = "temp_profile_square.png"
        img.save(temp_path)

        pdf.image(temp_path, x=15, y=5, h=40, w=40) 
        text_x_offset = 65 

    pdf.set_text_color(255, 255, 255)
    pdf.set_x(text_x_offset)
    pdf.set_font("Arial", 'B', 28)
    pdf.cell(0, 20, name.upper() if name else "YOUR NAME", ln=True, align='L' if profile_pic else 'C')
    
    pdf.set_x(text_x_offset)
    pdf.set_font("Arial", 'I', 14)
    pdf.cell(0, 10, role if role else "Professional Title", ln=True, align='L' if profile_pic else 'C')
    
    pdf.set_font("Arial", size=10)
    pdf.set_y(40) 
    pdf.cell(0, 10, f"Email: {email}  |  LinkedIn: {linkedin}", ln=True, align='C')
    pdf.ln(10)

    # TWO COLUMN CONTENT LAYOUT
    pdf.set_text_color(0, 0, 0)
    y_start = pdf.get_y()

    # LEFT COLUMN (Education & Skills)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_draw_color(r, g, b)
    pdf.cell(90, 10, "EDUCATION", ln=True)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(90, 8, education if education else "Education details...")
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(90, 10, "TECHNICAL SKILLS", ln=True)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.set_font("Arial", size=11)
    for skill in skills_list:
        if skill.strip():
            pdf.cell(5)
            pdf.cell(0, 7, f"- {skill.strip()}", ln=True)

    # RIGHT COLUMN (Work Experience)
    pdf.set_y(y_start)
    pdf.set_x(110)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(90, 10, "WORK EXPERIENCE", ln=True)
    pdf.set_x(110)
    pdf.line(110, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=11)
    for exp in experience_list:
        if exp.strip():
            pdf.set_x(110)
            pdf.multi_cell(90, 7, f"* {exp.strip()}")
            pdf.ln(2)

    return pdf.output()

# STREAMLIT APP
st.set_page_config(page_title="Resume Pro Builder", page_icon="📝", layout="wide")

if 'skills' not in st.session_state:
    st.session_state.skills = [""]
if 'experience' not in st.session_state:
    st.session_state.experience = [""]

with st.sidebar:
    st.header("🎨 Customize based on your Preference!")
    accent_color = st.color_picker("Choose Resume Accent Color", "#2E86C1")
    font_size = st.slider("Preview Font Size", 12, 30, 20)
    show_photo = st.checkbox("Include Profile Photo Space", value=True)
    st.divider()
    st.info("Choose color here and it will appear on the PDF version of your Resume(specifically on header):3")

st.title("Resume Builder 🧾")
tab_build, tab_about = st.tabs(["🏗️ Build Resume", "ℹ️ About This App"])

with tab_build:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Personal Information")
        full_name = st.text_input("Full Name", placeholder="Juan Dela Cruz")
        email = st.text_input("Email Address")
        profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])

    with col2:
        st.subheader("Professional Links")
        linkedin = st.text_input("LinkedIn URL")
        job_role = st.selectbox("Target Job Role", ["Software Engineer", "Data Analyst", "UI/UX Designer", "Network Admin", "CyberSecurity Analyst"])

    with st.expander("Work Experience Details", expanded=True):
        for i in range(len(st.session_state.experience)):
            cols = st.columns([4, 1])
            st.session_state.experience[i] = cols[0].text_input(f"Item {i+1}", value=st.session_state.experience[i], key=f"exp_{i}")
            if cols[1].button("🗑️", key=f"del_exp_{i}"):
                st.session_state.experience.pop(i)
                st.rerun()
        if st.button("➕ Add Experience"):
            st.session_state.experience.append("")
            st.rerun()

    with st.expander("Education & Skills", expanded=True):
        education = st.text_area("List your degrees")
        st.divider()
        st.write("### 🛠️ Skills List")
        for i in range(len(st.session_state.skills)):
            cols = st.columns([4, 1])
            st.session_state.skills[i] = cols[0].text_input(f"Skill {i+1}", value=st.session_state.skills[i], key=f"skill_{i}")
            if cols[1].button("🗑️", key=f"del_skill_{i}"):
                st.session_state.skills.pop(i)
                st.rerun()
        if st.button("➕ Add Skill"):
            st.session_state.skills.append("")
            st.rerun()

    if st.button("Generate Preview"):
        st.success("Resume Preview Generated!")
        st.divider()
        
        # Web Preview rendering
        st.markdown(f"<h1 style='color:{accent_color}; font-size:{font_size+10}px;'>{full_name}</h1>", unsafe_allow_html=True)
        st.write(f"**{job_role}** | {email}")
        
        res_col1, res_col2 = st.columns([1, 2])
        with res_col1:
            if show_photo and profile_pic:
                # Preview: this also uses auto-cropping for photo
                img_preview = Image.open(profile_pic)
                img_preview = ImageOps.fit(img_preview, (300, 300), centering=(0.5, 0.5))
                st.image(img_preview, width=150)
            st.markdown("### Skills")
            for s in st.session_state.skills: 
                if s: st.write(f"- {s}")
        
        with res_col2:
            st.markdown("### Experience")
            for e in st.session_state.experience: 
                if e: st.write(f"- {e}")
            st.markdown("### Education")
            st.write(education)
        
        st.divider()
        pdf_bytes = create_pdf(full_name, email, linkedin, job_role, st.session_state.experience, education, st.session_state.skills, accent_color, profile_pic)
        st.download_button(label="📥 Download Structured PDF", data=bytes(pdf_bytes), file_name="resume.pdf", mime="application/pdf")

with tab_about:
    st.header("Welcome to Resume Builder App!")

    st.subheader("⚙️ What exactly does this app do?")
    st.write("""
    * Takes your skills, education, and achievements and organizes them automatically.
    * Converts information into a well-structured PDF resume.
    * Handles the formatting and layout so you don’t have to design it yourself.
    """)

    st.subheader("👥 Who is this for?")
    st.write("""
   * Students who are preparing their first resume.
   * People who want a ready-to-use resume in just a few minutes without spending hours designing it.

    """)

    st.subheader("📂 How does it work?")
    st.markdown("""
    **What you give us (Inputs):**
    * Your basics (Name, Email, LinkedIn).
    * A profile picture.
    * Your target job role.
    * Lists of your achievements, skills, and education history.
    
    **What you get (Output):**
    * A **live preview** so you can see how you look on paper.
    * A **structured, professional PDF** that you can download right away! 🚀
    """)
    
    st.write("---")
    st.write("Hope this makes your job hunting a little easier! :)")