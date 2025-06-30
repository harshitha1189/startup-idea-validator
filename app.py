import streamlit as st
import chromadb
import requests
from urllib.parse import quote
import uuid

# === Initialize Vector DB ===
@st.cache_resource
def init_chroma():
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name="startup_ideas",
        metadata={"hnsw:space": "cosine"}
    )
    return collection

# === Call SkillCaptain LLM API ===
def call_skillcaptain_api(prompt, user_id="12"):
    encoded_prompt = quote(prompt)
    url = f"https://skillcaptain.app/unicorn/p/llm/openai?userId={user_id}&prompt={encoded_prompt}"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else f"Error: {response.status_code}"
    except Exception as e:
        return f"Error calling API: {str(e)}"

# === Add to ChromaDB ===
def add_document_to_vector_db(collection, text, metadata=None):
    doc_id = str(uuid.uuid4())
    collection.add(
        documents=[text],
        metadatas=[metadata or {}],
        ids=[doc_id]
    )
    return doc_id

# === Search Vector DB ===
def search_similar_documents(collection, query, n_results=3):
    return collection.query(query_texts=[query], n_results=n_results)

# === RAG Prompt Creation ===
def create_rag_prompt(idea, context_docs):
    context = "\n\n".join(context_docs)
    return f"""You are an AI startup advisor. Use the following past case studies to analyze the new startup idea. Suggest potential, risks, and improvements.

Context:
{context}

New Startup Idea: {idea}

AI Advisor Response:"""

# === Streamlit UI ===
st.set_page_config("🚀 Startup Idea Validator", page_icon="💡")
st.title("🚀 Startup Idea Validator with RAG")
st.markdown("Validate your startup idea using AI + case study knowledge base (RAG).")

collection = init_chroma()

tab1, tab2, tab3 = st.tabs(["📥 Add Case Studies", "🔍 Search Similar Ideas", "💬 Validate My Idea"])

# === Tab 1: Add Startup Case Studies ===
with tab1:
    st.subheader("📥 Add Startup Case Study")
    title = st.text_input("Case Study Title")
    content = st.text_area("Describe the business, its market, growth factors, or challenges", height=150)

    if st.button("Add Case Study"):
        if title and content:
            doc_id = add_document_to_vector_db(collection, content, {"title": title})
            st.success(f"✅ Added: {title} (ID: {doc_id[:8]}...)")
        else:
            st.warning("⚠️ Please enter both title and content")

# === Tab 2: Search ===
with tab2:
    st.subheader("🔍 Search Similar Startup Ideas")
    query = st.text_input("Search Topic (e.g., 'AI education', 'pet care delivery')")

    if st.button("Search Ideas"):
        results = search_similar_documents(collection, query, 3)
        if results['documents'][0]:
            for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                with st.expander(f"Idea {i+1}: {meta.get('title', 'Untitled')}"):
                    st.write(doc)
        else:
            st.info("No similar ideas found. Try adding more case studies.")

# === Tab 3: RAG - Validate Startup Idea ===
with tab3:
    st.subheader("💬 Validate Your Startup Idea")
    idea_input = st.text_area("Describe your startup idea in 2-3 lines", height=100)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔗 Validate with RAG"):
            if idea_input:
                results = search_similar_documents(collection, idea_input, 2)
                docs = results['documents'][0]

                if docs:
                    prompt = create_rag_prompt(idea_input, docs)
                    response = call_skillcaptain_api(prompt)
                    st.subheader("🧠 AI's Feedback with RAG")
                    st.write(response)
                else:
                    st.warning("No context found. Try adding more case studies.")
            else:
                st.warning("Enter your startup idea first.")

    with col2:
        if st.button("🎯 Direct LLM Validation (No RAG)"):
            if idea_input:
                response = call_skillcaptain_api(idea_input)
                st.subheader("🧠 AI's Feedback without Context")
                st.write(response)
            else:
                st.warning("Enter your startup idea first.")

# === Sidebar Info ===
st.sidebar.markdown("### ℹ️ Project Info")
st.sidebar.markdown("**Project:** Startup Validator with RAG")
st.sidebar.markdown(f"📄 Total Case Studies: **{collection.count()}**")



# import streamlit as st
# import chromadb
# import requests
# from urllib.parse import quote
# import uuid
# import json

# # Initialize ChromaDB client
# @st.cache_resource
# def init_chroma():
#     client = chromadb.Client()
#     # Create or get collection
#     collection = client.get_or_create_collection(
#         name="knowledge_base",
#         metadata={"hnsw:space": "cosine"}
#     )
#     return collection

# def call_skillcaptain_api(prompt, user_id="12"):
#     """Call the SkillCaptain API with the given prompt"""
#     encoded_prompt = quote(prompt)
#     url = f"https://skillcaptain.app/unicorn/p/llm/openai?userId={user_id}&prompt={encoded_prompt}"
    
#     headers = {
#         'Content-Type': 'application/json',
#         'Cookie': 'JSESSIONID=12BF1CED08EEB7E65474CDBDC035CC80; JSESSIONID=069873E02C6EE8E47E2F2547FE9938E0'
#     }
    
#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.text
#         else:
#             return f"Error: {response.status_code} - {response.text}"
#     except Exception as e:
#         return f"Error calling API: {str(e)}"

# def add_document_to_vector_db(collection, text, metadata=None):
#     """Add a document to the vector database"""
#     doc_id = str(uuid.uuid4())
#     collection.add(
#         documents=[text],
#         metadatas=[metadata or {}],
#         ids=[doc_id]
#     )
#     return doc_id

# def search_similar_documents(collection, query, n_results=3):
#     """Search for similar documents in the vector database"""
#     results = collection.query(
#         query_texts=[query],
#         n_results=n_results
#     )
#     return results

# def create_rag_prompt(query, context_docs):
#     """Create a RAG prompt combining query and retrieved context"""
#     context = "\n\n".join([doc for doc in context_docs])
    
#     rag_prompt = f"""Based on the following context information, please answer the question. If the context doesn't contain relevant information, say so clearly.
# Context:
# {context}
# Question: {query}
# Answer:"""
    
#     return rag_prompt

# # Streamlit UI
# st.title("🤖 RAG Demo: Vector DB + LLM")
# st.markdown("### Learn how Retrieval-Augmented Generation works!")

# # Initialize ChromaDB
# collection = init_chroma()

# # Sidebar for configuration
# st.sidebar.header("Configuration")
# user_id = st.sidebar.text_input("User ID", value="12")

# # Main tabs
# tab1, tab2, tab3, tab4 = st.tabs(["📚 Add Knowledge", "🔍 Search Vector DB", "💬 Ask Questions", "🎓 Compare Responses"])

# with tab1:
#     st.header("Step 1: Build Your Knowledge Base")
#     st.markdown("Add documents to the vector database. These will be used as context for RAG.")
    
#     sample_docs = {
#         "Machine Learning Basics": "...",
#         "Deep Learning": "...",
#         "Natural Language Processing": "...",
#         "Computer Vision": "..."
#     }
    
#     st.subheader("Quick Add: Sample Documents")
#     for title, content in sample_docs.items():
#         if st.button(f"Add: {title}"):
#             doc_id = add_document_to_vector_db(
#                 collection, 
#                 content, 
#                 {"title": title, "source": "sample"}
#             )
#             st.success(f"Added '{title}' to knowledge base! ID: {doc_id[:8]}...")
    
#     st.subheader("Add Custom Document")
#     doc_title = st.text_input("Document Title")
#     doc_content = st.text_area("Document Content", height=150)
    
#     if st.button("Add Custom Document"):
#         if doc_content and doc_title:
#             doc_id = add_document_to_vector_db(
#                 collection, 
#                 doc_content, 
#                 {"title": doc_title, "source": "custom"}
#             )
#             st.success(f"Added '{doc_title}' to knowledge base! ID: {doc_id[:8]}...")
#         else:
#             st.error("Please provide both title and content")

# with tab2:
#     st.header("Step 2: Search the Vector Database")
#     st.markdown("See how vector similarity search works - the core of RAG!")
    
#     search_query = st.text_input("Search Query", placeholder="e.g., 'neural networks'")
#     num_results = st.slider("Number of results", 1, 5, 3)
    
#     if st.button("Search") and search_query:
#         with st.spinner("Searching vector database..."):
#             results = search_similar_documents(collection, search_query, num_results)
            
#             if results['documents'][0]:
#                 st.subheader("Search Results:")
#                 for i, (doc, metadata, distance) in enumerate(zip(
#                     results['documents'][0], 
#                     results['metadatas'][0], 
#                     results['distances'][0]
#                 )):
#                     with st.expander(f"Result {i+1} - Similarity: {1-distance:.3f}"):
#                         st.write(f"**Title:** {metadata.get('title', 'Untitled')}")
#                         st.write(f"**Content:** {doc}")
#                         st.write(f"**Distance:** {distance:.3f}")
#             else:
#                 st.info("No documents found. Add some documents first!")

# with tab3:
#     st.header("Step 3: RAG in Action")
#     st.markdown("Ask questions and see how RAG uses retrieved context to answer!")
    
#     user_question = st.text_input("Your Question", placeholder="e.g., 'What is deep learning?'")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         if st.button("Answer with RAG"):
#             if user_question:
#                 with st.spinner("Retrieving relevant documents..."):
#                     search_results = search_similar_documents(collection, user_question, 2)
                    
#                     if search_results['documents'][0]:
#                         retrieved_docs = search_results['documents'][0]
#                         rag_prompt = create_rag_prompt(user_question, retrieved_docs)
                        
#                         st.subheader("🔍 Retrieved Context:")
#                         for i, doc in enumerate(retrieved_docs):
#                             st.text_area(f"Document {i+1}", doc, height=100, disabled=True)
                        
#                         st.subheader("🤖 RAG Response:")
#                         with st.spinner("Getting AI response..."):
#                             response = call_skillcaptain_api(rag_prompt, user_id)
#                             st.write(response)
#                     else:
#                         st.warning("No relevant documents found in the knowledge base!")
#             else:
#                 st.error("Please enter a question")
    
#     with col2:
#         if st.button("Answer without RAG"):
#             if user_question:
#                 st.subheader("🤖 Direct LLM Response:")
#                 with st.spinner("Getting AI response..."):
#                     response = call_skillcaptain_api(user_question, user_id)
#                     st.write(response)
#             else:
#                 st.error("Please enter a question")

# with tab4:
#     st.header("Step 4: Compare RAG vs Direct LLM")
#     st.markdown("See the difference between RAG-enhanced and direct LLM responses!")
    
#     comparison_question = st.text_input("Question for Comparison", placeholder="e.g., 'Explain computer vision'")
    
#     if st.button("Compare Responses"):
#         if comparison_question:
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("🔗 RAG Response")
#                 with st.spinner("Generating RAG response..."):
#                     search_results = search_similar_documents(collection, comparison_question, 2)
#                     if search_results['documents'][0]:
#                         retrieved_docs = search_results['documents'][0]
#                         rag_prompt = create_rag_prompt(comparison_question, retrieved_docs)
#                         rag_response = call_skillcaptain_api(rag_prompt, user_id)
                        
#                         st.write("**Context Used:**")
#                         for i, doc in enumerate(retrieved_docs):
#                             st.text_area(f"Context {i+1}", doc[:200] + "...", height=80, disabled=True, key=f"rag_context_{i}")
                        
#                         st.write("**Response:**")
#                         st.write(rag_response)
#                     else:
#                         st.warning("No context found for RAG")
            
#             with col2:
#                 st.subheader("🎯 Direct LLM Response")
#                 with st.spinner("Generating direct response..."):
#                     direct_response = call_skillcaptain_api(comparison_question, user_id)
#                     st.write("**Response:**")
#                     st.write(direct_response)
#         else:
#             st.error("Please enter a question for comparison")

# # Footer
# st.markdown("---")
# st.markdown("""
# ### 🎓 What You've Learned:
# 1. **Vector Databases**: Store and search documents using semantic similarity  
# 2. **Retrieval**: Find relevant context based on user queries  
# 3. **Augmentation**: Enhance LLM prompts with retrieved context  
# 4. **Generation**: Get more accurate, contextual responses  

# **Key RAG Benefits:**
# - Reduces hallucinations by grounding responses in real data  
# - Enables domain-specific knowledge without retraining  
# - Keeps information current and verifiable
# """)

# # Sidebar count
# total_docs = collection.count()
# st.sidebar.markdown(f"**Knowledge Base:** {total_docs} documents")