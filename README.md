# 🤖 AI Learning Assistant

Welcome to the **AI Learning Assistant** – an intelligent research assistant built using Streamlit and LLaMA3 (via Groq API) that generates **comprehensive, research-based educational reports**. This tool is perfect for learners, students, and researchers who want deep, structured, and referenced content on various topics powered by AI.

---

## 📌 Features

- ✅ Research-based multi-page reports with proper structure
- ✅ Each section contains a **minimum of 200–250 words**
- ✅ Includes **real-time statistics**, trends, and innovations
- ✅ Generates **5–7 accessible references** with links
- ✅ Suggests **3–4 recommended learning resources**
- ✅ Covers core concepts, use cases, ethics, and challenges
- ✅ Visual aids (charts, graphs) optionally included

---

## 🔄 Process Workflow

### 1. Topic Input
The user enters a topic (e.g., "Artificial Intelligence").

### 2. Prompt Engineering
A dynamic and advanced prompt is generated, instructing the LLM to create:
- 6–7 sections (200–250 words each)
- Statistics and citations
- 5–7 academic references
- 3–4 learning resources

### 3. LLM Integration via Groq API
- Uses `llama3-70b-8192` model via **Groq API** for fast, high-quality response
- Sends the prompt using `requests` with your Groq API key

### 4. Response Handling
- The model’s response is parsed and formatted
- Sections are separated and titles identified

### 5. Report Display in Streamlit
- Streamlit dynamically displays the output with proper formatting
- Includes expanders, scrollable containers, and optional charts

### 6. (Optional) Future Export
- Plans to add PDF/Markdown export of the report  
- Integration of real-time web scraping and citation validation is in the roadmap

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-learning-assistant.git
cd ai-learning-assistant
