# 📄 Automated Academic Peer-Review Assistant
**Live Demo:** [Click here to try the app!](https://gemini-reviewer-app.streamlit.app/)

Built for the **Best Use of Gemini API** Hackathon. 

## 💡 The Inspiration
Academic peer review is the backbone of scientific progress, but the process is currently a massive bottleneck. As researchers and active peer reviewers for highly rigorous publications (like *Expert Systems with Applications*), evaluating dense, 30-page engineering and AI manuscripts takes hours of intense focus. Reviewers are overwhelmed, and incredible research gets delayed. I wanted to see if the Gemini API could fix this.

## 🚀 The Solution
This application is an AI co-pilot designed specifically for academic researchers. It instantly ingests complex technical PDFs, synthesizes the core contributions, flags methodological flaws, and provides an interactive chat interface to interrogate the data—turning hours of reading into minutes of high-level analysis.

## ✨ Key Features
* **Native PDF Understanding (Zero OCR):** Utilizes the Gemini File API to read full research papers natively. It preserves the layout, data tables, and complex mathematical contexts without relying on clunky third-party text extractors.
* **Structured Evaluation Generation:** Uses advanced prompt engineering to force the LLM into an expert persona, outputting a standardized, journal-ready review draft (Executive Summary, Methodological Strengths, Major Concerns, Recommendation).
* **Interactive Document Q&A:** Chat directly with the document's memory. Ask highly specific follow-ups like, *"Does their deep learning approach address the class imbalance in the dataset?"* and get immediate, contextual answers.

## 🛠️ Tech Stack
* **Frontend/Backend:** [Streamlit](https://streamlit.io/) (Python) for rapid, stateful web app deployment.
* **AI Engine:** Google Gemini (`gemini-2.5-flash` via `google-generativeai` SDK). Chosen specifically for its massive context window, blazing-fast inference speed, and native multimodal document processing capabilities.

## ⚙️ Run It Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rass89/gemini-reviewer-app.git
   cd gemini-reviewer-app
