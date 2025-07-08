
# 🚀 Startup Idea Validator

An AI-powered Streamlit web app that validates startup ideas by analyzing user-inputted descriptions, extracting core concepts, and comparing them with real-world career and skill datasets using a vector database (ChromaDB) and Retrieval-Augmented Generation (RAG) techniques.

## 🔍 Features

- ✅ Intelligent analysis of startup descriptions
- 📊 Skill and domain extraction using NLP
- 🔁 RAG pipeline powered by ChromaDB and SkillCaptain API
- 🧠 Optional integration with local LLMs (e.g., HuggingFace models)
- 📂 Resume and skill match evaluation
- 🎯 Smart suggestions for career feasibility and market alignment

## 🛠️ Tech Stack

| Category        | Technologies Used                                |
|----------------|---------------------------------------------------|
| Frontend       | Streamlit                                         |
| Backend        | Python, ChromaDB, Langchain                       |
| NLP / AI       | HuggingFace Transformers, SentenceTransformers    |
| API            | SkillCaptain Public API                           |
| Storage        | Local Vector Store (ChromaDB)                     |
| Version Control| Git, GitHub                                       |


## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/harshitha1189/startup-idea-validator.git
cd to the path
````

### 2. Set Up Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

## 🔧 APIs Used

* [SkillCaptain API](https://skillcaptain.com/api-docs) — For skill mapping and recommendations

## Use Cases: Startup Idea Validator
🔹 Tab 1: Describe Your Startup Idea
💡 Users enter a plain-text description of their startup idea.
🧠 The system uses NLP techniques to extract core skills, keywords, and relevant domains.
✅ Helps entrepreneurs clarify and structure their ideas, identifying what technical and domain expertise is needed.

🔹 Tab 2: Match Skills with Career & Industry Paths
📚 Extracted skills are sent to a Retrieval-Augmented Generation (RAG) pipeline using ChromaDB.
🔗 Matches these skills to industry trends and roles via the SkillCaptain API.
🔍 Useful for validating the viability of a startup idea based on real-world job and tech trends.

🔹 Tab 3: Compare RAG vs Direct LLM Response
🤖 This tab highlights the difference between a direct LLM response (without external context) vs a RAG-enhanced response (with external knowledge from the vector DB).
📚 Shows how integrating relevant, up-to-date information improves the depth and accuracy of AI-generated career or business suggestions.
🎯 Educates users on the power of context-aware AI in validating startup ideas and making data-driven decisions.

## 📈 Future Enhancements

* 🌐 Deploy on Streamlit Cloud or HuggingFace Space
* 🧠 Integrate OpenAI GPT-4/Claude for better validation logic

## 🤝 Contributing

Feel free to fork the repo, submit pull requests, or create issues for suggestions!


### 👩‍💻 Built by [@harshitha1189](https://github.com/harshitha1189)

