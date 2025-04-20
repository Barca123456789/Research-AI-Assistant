import os
from typing import Dict
from groq import Groq
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from fpdf import FPDF
import streamlit as st
import base64
import requests
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

def ask_user_preferences_ui() -> Dict:
    st.title("📘 AI Learning Assistant")
    st.markdown("Enter your learning preferences to generate a personalized report.")

    topic = st.text_input("🔍 What topic do you want to learn about?")
    goal = st.text_input("🎯 What is your learning objective? (e.g., understand basics, advanced mastery, career prep)")
    level = st.selectbox("📚 What is your current knowledge level?", ["Beginner", "Intermediate", "Advanced"])

    if topic and goal:
        return {
            "topic": topic.strip().lower(),
            "goal": goal.strip(),
            "level": level.strip()
        }
    else:
        return {}

def simulate_sources(topic: str) -> Dict:
    base_topic = topic.lower().replace(" ", "+")
    return {
        "web": [
            {
                "title": f"{topic.title()} Basics Explained",
                "link": f"https://www.ibm.com/topics/{base_topic}",
                "summary": f"Introduction to {topic.title()} and its applications."
            },
            {
                "title": f"The Business Side of {topic.title()}",
                "link": f"https://www.mckinsey.com/search?q={base_topic}",
                "summary": f"Impact of {topic.title()} in industries."
            }
        ],
        "academic": [
            {
                "title": f"Recent Research in {topic.title()}",
                "link": f"https://scholar.google.com/scholar?q={base_topic}+2023",
                "summary": f"Academic insights on {topic.title()} from recent studies."
            }
        ],
        "videos": [
            {
                "title": f"{topic.title()} in 5 Minutes",
                "link": f"https://www.youtube.com/results?search_query={base_topic}+introduction",
                "transcript": f"This video explains key concepts of {topic.title()}..."
            }
        ]
    }

def gather_information(topic: str) -> Dict:
    return simulate_sources(topic)

def generate_report(user_input: Dict, sources: Dict) -> str:
    prompt = f"""
You are an expert academic writer tasked with creating a comprehensive, deeply researched educational report on the topic **'{user_input['topic']}'**. The report should cater to a learner with **{user_input['level']}** knowledge level, aiming to **{user_input['goal']}**.

**Report Formatting Rules**:
- All **titles and subheadings** should be in bold.
- All **links should be properly hyperlinked**, formatted as `[Title](https://link.com)`.
- Ensure all hyperlinks point to authentic, working, and valid URLs from trusted domains like `.edu`, `.org`, `.gov`, scholarly databases, or reputed companies.
- Each subsection point under every heading should be **numbered** (e.g., 1.1, 1.2...).
- Visual Aids section should include a plot titled 'Material Strength Comparison'.

**Report Specifications**:
- **Length**: At least 2-3 pages.
- **Section Length**: Each section should contain 200-250 words.
- **References**: Include 5-7 authentic sources with accessible hyperlinks and **uniform formatting**.
- **Recommended Learning Resources**: Suggest 3-4 reputable books, websites, or courses with clickable hyperlinks and **proper numbering**.

**Report Structure**:
**1. Introduction**: Define the topic, its importance, and context.
**2. Core Concepts and Theoretical Foundations**: Explain key ideas, frameworks, and terminology with examples.
**3. Recent Trends, Innovations, and Statistics**: Include current research, breakthroughs, and real-world statistics with sources.
**4. Applications and Use Cases**: Describe real-world applications across different domains.
**5. Challenges and Ethical Considerations**: Discuss limitations, challenges, or controversies.
**6. Visual Aids**: Describe diagrams/figures or suggest chart types with sample data and incorporate a plot for 'Material Strength Comparison'.
**7. Summary**: Recap key takeaways in bullet points.
**8. References**: List 5-7 authentic sources with valid hyperlinks and titles (**uniformly formatted and numbered**).
**9. Recommended Learning Resources**: Suggest 3-4 books, websites, video lectures, or online courses with **numbering and equal formatting**.

**Background Information from Simulated Sources**:
- Web content: {sources.get('web', [])}
- Academic content: {sources.get('academic', [])}
- Video transcript: {sources.get('videos', [])}

Please generate the report adhering strictly to the formatting rules and structure above.
    """

    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a highly knowledgeable AI academic writer."},
            {"role": "user", "content": prompt}
        ]
    )

    return chat_completion.choices[0].message.content

def generate_image_from_prompt(prompt: str, figure_number: int) -> str:
    categories = ['Carbon Nanotube', 'Graphene', 'Copper Nanoparticle']
    strengths = [63, 130, 20]  # MPa

    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, strengths, color='dodgerblue')
    plt.title('Material Strength Comparison', fontsize=14, weight='bold')
    plt.xlabel('Nanomaterial', fontsize=12, weight='bold')
    plt.ylabel('Strength (MPa)', fontsize=12, weight='bold')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval}', ha='center', va='bottom', fontsize=10)

    filename = f"figure_{figure_number}.png"
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def display_figure_in_streamlit(image_path: str, caption: str, figure_number: int):
    st.image(image_path, use_container_width=True)
    st.markdown(f"<div style='text-align:center; font-style:italic;'><b>Figure {figure_number}: {caption}</b></div>", unsafe_allow_html=True)

def export_to_pdf(report: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in report.split('\n'):
        if line.startswith("**") and line.endswith("**"):
            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 10, line.replace("**", ""))
            pdf.set_font("Arial", size=12)
        else:
            pdf.multi_cell(0, 10, line)

    if os.path.exists("figure_1.png"):
        pdf.image("figure_1.png", x=10, y=None, w=180)
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "Figure 1: Visual Representation", ln=True, align='C')

    try:
        pdf.output("AI_Learning_Report.pdf")
        st.success("✅ PDF report saved as 'AI_Learning_Report.pdf'")
    except PermissionError:
        st.error("❌ Permission denied: Please close the 'AI_Learning_Report.pdf' if it's open and try again.")

def main():
    user_input = ask_user_preferences_ui()
    if user_input:
        sources = gather_information(user_input['topic'])
        st.info("Generating your personalized research-based report...")
        report = generate_report(user_input, sources)

        with st.expander("📄 View Report"):
            st.markdown(report, unsafe_allow_html=True)

        figure_number = 1
        prompt = f"{user_input['topic'].title()} Adoption by Industry"
        image_path = generate_image_from_prompt(prompt, figure_number)
        caption = f"{user_input['topic'].title()} Visual Representation"
        display_figure_in_streamlit(image_path, caption, figure_number)

        if st.button("📥 Export Report to PDF"):
            export_to_pdf(report)

if __name__ == "__main__":
    main()