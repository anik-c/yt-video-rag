# YouTube Video RAG (Retrieval-Augmented Generation)

A Streamlit-based application that extracts transcripts from YouTube videos and enables users to ask questions about the video content using Google's Generative AI models.

## 🚀 Features

- **YouTube Transcript Extraction**: Automatically fetches transcripts from YouTube videos using video IDs
- **Smart Text Chunking**: Splits long transcripts into manageable chunks for better processing
- **Vector Search**: Uses FAISS vector store for efficient similarity search across transcript content
- **AI-Powered Q&A**: Leverages Google's Gemini AI model to answer questions based on video content
- **User-Friendly Interface**: Clean Streamlit web interface for easy interaction

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: Framework for building applications with large language models
- **Google Generative AI**: Gemini Pro model for chat responses and embeddings
- **FAISS**: Vector database for similarity search
- **YouTube Transcript API**: For extracting video transcripts
- **Python-dotenv**: Environment variable management

## 📋 Prerequisites

- Python 3.8 or higher
- Google API key for Generative AI
- Internet connection for YouTube transcript fetching

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd yt-video-rag
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if using uv:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🎯 Usage

1. **Run the application**:
   ```bash
   streamlit run main.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:8501`

3. **Use the application**:
   - Enter a YouTube video ID in the input field
   - The application will extract the transcript and create a searchable vector database
   - Ask questions about the video content
   - Get AI-powered answers based on the transcript

## 📖 How It Works

1. **Transcript Extraction**: The app uses the YouTube Transcript API to fetch transcripts for the provided video ID
2. **Text Processing**: The transcript is split into chunks using RecursiveCharacterTextSplitter for optimal processing
3. **Vector Storage**: Text chunks are converted to embeddings and stored in a FAISS vector database
4. **Question Answering**: When a user asks a question, the system:
   - Finds relevant transcript chunks using similarity search
   - Provides context to the Gemini AI model
   - Generates accurate answers based strictly on the video content

## 🔧 Configuration

### Model Settings
- **Chat Model**: Gemini 2.5 Flash with temperature 0.7
- **Embeddings**: Google Generative AI Embeddings (embedding-001)
- **Chunk Size**: 1000 characters with 200 character overlap

### Error Handling
The application handles various scenarios:
- Transcripts disabled for the video
- No transcript found for the requested language
- Video unavailable
- General API errors

## 📝 Example Usage

1. Find a YouTube video URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
2. Extract the video ID: `dQw4w9WgXcQ`
3. Paste the video ID into the application
4. Ask questions like:
   - "What is the main topic of this video?"
   - "Can you summarize the key points?"
   - "What does the speaker say about [specific topic]?"

## ⚠️ Limitations

- Only works with videos that have English transcripts available
- Answers are limited to content present in the video transcript
- Some videos may have transcripts disabled by the creator
- API rate limits may apply based on your Google API usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Google AI](https://ai.google/) for the generative AI capabilities
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Note**: Make sure to keep your Google API key secure and never commit it to version control. Always use environment variables for sensitive information.
