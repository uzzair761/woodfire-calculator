import streamlit as st

# ---------- VIDEO BACKGROUND ----------
video_url = "https://youtu.be/wKjIYlaSnEA"  # replace with your own mp4 link

st.markdown(
    f"""
    <style>
    .video-container {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        overflow: hidden;
    }}

    .video-container video {{
        position: absolute;
        top: 50%;
        left: 50%;
        min-width: 100%;
        min-height: 100%;
        width: auto;
        height: auto;
        transform: translate(-50%, -50%);
        object-fit: cover;
    }}

    .stApp {{
        background: transparent;
    }}
    </style>

    <div class="video-container">
        <video autoplay muted loop playsinline>
            <source src="{video_url}" type="video/mp4">
        </video>
    </div>
    """,
    unsafe_allow_html=True
)

