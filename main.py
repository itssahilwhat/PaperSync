import streamlit as st
from fetch_data import fetch_youtube_explanations, fetch_github_implementations

# Page configuration
st.set_page_config(
    page_title="PaperSync",
    page_icon="📖",
    layout="wide"
)

# Load custom fonts and icons
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
""", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        font-family: 'Inter', sans-serif;
        padding: 1rem;
    }

    .welcome-text {
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }

    .resource-card {
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 1rem;
        background-color: #fff;
        transition: box-shadow 0.2s ease;
    }

    .resource-card:hover {
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .youtube-icon {
        color: #ff0000;
        margin-right: 0.5rem;
    }

    .github-icon {
        color: #333;
        margin-right: 0.5rem;
    }

    .card-title a {
        font-size: 1.1rem;
        font-weight: 600;
        color: #007bff;
        text-decoration: none;
    }

    .card-title a:hover {
        text-decoration: underline;
    }

    .card-meta {
        font-size: 0.9rem;
        color: #666;
        margin: 0.5rem 0;
    }

    .card-desc {
        font-size: 0.85rem;
        color: #777;
    }

    .stats {
        display: flex;
        gap: 1rem;
        font-size: 0.9rem;
        color: #555;
    }

    .footer-note {
        text-align: center;
        font-size: 0.8rem;
        color: #666;
        margin-top: 2rem;
    }

    .sidebar .sidebar-content {
        padding: 1rem;
    }

    div.stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

def render_youtube_card(video):
    """Render a YouTube video card."""
    st.markdown(f"""
    <div class="resource-card">
        <div class="card-title">
            <i class="fab fa-youtube youtube-icon"></i>
            <a href="{video['link']}" target="_blank">{video['title']}</a>
        </div>
        <div class="card-meta">{video['channel']} • {video['views']} • {video['published']}</div>
        <img src="{video['thumbnail']}" style="width: 160px; height: 90px; border-radius: 4px; margin-top: 0.5rem;">
    </div>
    """, unsafe_allow_html=True)

def render_github_card(repo):
    """Render a GitHub repository card."""
    st.markdown(f"""
    <div class="resource-card">
        <div class="card-title">
            <i class="fab fa-github github-icon"></i>
            <a href="{repo['link']}" target="_blank">{repo['title']}</a>
        </div>
        <div class="card-meta">{repo['creator']} • {repo['language']}</div>
        <div class="card-desc">{repo['summary']}</div>
        <div class="stats">
            <span>★ {repo['stars']}</span>
            <span>⑂ {repo['forks']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function."""
    # Header
    st.title("PaperSync")
    st.markdown("Discover video explanations and code implementations for research papers.")

    # Sidebar search form
    with st.sidebar:
        st.header("Search Papers")
        with st.form("explore_form"):
            research_query = st.text_input("Research Paper Name", placeholder="e.g., 'Attention is All You Need'")
            search_clicked = st.form_submit_button("Explore")

    # Main content
    if not search_clicked or not research_query:
        st.markdown('<div class="welcome-text">Use the sidebar to search for a research paper.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Searching for resources..."):
            youtube_results = fetch_youtube_explanations(research_query)
            github_projects = fetch_github_implementations(research_query)

        # Display results in tabs
        tab_youtube, tab_github = st.tabs(["🎥 YouTube Explanations", "💻 GitHub Implementations"])

        with tab_youtube:
            if youtube_results:
                for video in youtube_results:
                    render_youtube_card(video)
            else:
                st.info("No YouTube explanations found for this paper.")

        with tab_github:
            if github_projects:
                for repo in github_projects:
                    render_github_card(repo)
            else:
                st.info("No GitHub implementations found for this paper.")

    # Footer
    st.markdown('<div class="footer-note">Results sourced from YouTube and GitHub</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
