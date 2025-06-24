from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

st.write("### Youtube Video RAG")
st.write("➡️ The **video ID** is this part of a YouTube link: `https://www.youtube.com/watch?v=`**`videoid`**")

video_id=st.text_input("Paste the Youtube Video ID.")

if video_id:  # Only run if there's actual input
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript=" ".join(chunk['text'] for chunk in transcript_list)
        st.write(transcript)
    except TranscriptsDisabled:
        st.write("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        st.write("No transcript found for the requested language.")
    except VideoUnavailable:
        st.write("The video is unavailable.")
    except Exception as e:
        st.write(f"An unexpected error occurred: {e}")
