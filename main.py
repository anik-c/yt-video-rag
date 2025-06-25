import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate  
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from dotenv import load_dotenv

load_dotenv()

# Create a prompt template for the AI assistant
prompt=PromptTemplate(
    template="""
    You are a helpful assistant that answers questions based strictly on the provided YouTube video transcript context. Use the transcript chunks to generate answers that are accurate and relevant to what was said in the video. You may lightly polish the language for clarity and flow, but do not add any facts that are not present in the transcript.

    If the user's question is **not covered** or **not clearly addressed** in the transcript, politely respond that the transcript does not contain enough information to answer their question accurately.

    Transcript Context:
    {context}

    User Question:
    {question}

    Instructions:
    - If the answer is clearly in the context, explain it clearly, concisely, and in a user-friendly tone.
    - If the transcript offers partial information, explain only what is known, and indicate what’s missing.
    - If the question goes beyond the transcript, say:  
     “The transcript does not contain information to answer that accurately. Please provide more context or refer to another source.”
    """  ,
    input_variables=['context','question']  # Variables to be inserted into the prompt
)

# Initialize the Google Generative AI chat model
model=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Using Gemini Pro model for chat responses
    temperature=0.7
)

# Initialize embeddings model for converting text to vector representations
embedding_model=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

parser=StrOutputParser()

st.title("Youtube Video RAG") 

# Get video ID input from user
st.sidebar.write("➡️ The **video ID** is this part of a YouTube link: `https://www.youtube.com/watch?v=`**`videoid`**")
video_id=st.sidebar.text_input("Paste the Youtube Video ID.")

# Initialize transcript variable
transcript = None

# Process the video only if user has provided input
if video_id: 
    try:
        # Fetch transcript from YouTube using the video ID
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Join all transcript chunks into a single string
        transcript=" ".join(chunk['text'] for chunk in transcript_list)
   
    except TranscriptsDisabled:
        st.write("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        st.write("No transcript found for the requested language.")
    except VideoUnavailable:
        st.write("The video is unavailable.")
    except Exception as e:
        st.write(f"An unexpected error occurred: {e}")
        
# Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     with st.chat_message("assistant"):
#         st.markdown()

# Only process if transcript exists
if transcript:
    splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    chunks=splitter.create_documents([transcript])
    vector_store=FAISS.from_documents(chunks,embedding_model)

    retriever=vector_store.as_retriever(search_type="similarity",search_kwargs={"k":2})
            
    def format_docs(retrieved_docs):
        context_text="\n\n".join(doc.page_content for doc in retrieved_docs)
        return context_text

    parallel_chain=RunnableParallel({
        'context':retriever | RunnableLambda(format_docs),
        'question':RunnablePassthrough()
    })

    main_chain=parallel_chain | prompt | model | parser
    
    st.write(main_chain.invoke('Is Deepseek a chinese company?'))