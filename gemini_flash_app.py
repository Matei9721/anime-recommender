import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

MAL_API_URL = "https://api.myanimelist.net/v2"
MAL_CLIENT_ID = os.getenv("MAL_CLIENT_ID")

st.set_page_config(page_title="MyAnimeList Dashboard", layout="wide")

def fetch_user_animelist(username):
    """Fetches user's anime list with ratings."""
    try:
        headers = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}
        url = f"{MAL_API_URL}/users/{username}/animelist?fields=list_status,genres,num_episodes,score&limit=1000"  # Added 'score' field
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get('data', [])
        anime_list = []
        for anime_entry in data:
            anime = anime_entry.get('node', {})
            list_status = anime_entry.get('list_status', {})
            anime_list.append({
                'title': anime.get('title', ''),
                'genres': [genre.get('name', '') for genre in anime.get('genres', [])],
                'status': list_status.get('status', ''),
                'num_episodes': anime.get('num_episodes', 0),
                'score': list_status.get('score', 0),  # Extract the score
            })
        return pd.DataFrame(anime_list)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from MyAnimeList: {e}")
        return None
    except (KeyError, AttributeError, TypeError) as e:
        st.error(f"Error parsing data from MyAnimeList: {e}. The user might not exist or the API response changed. Check the API response format.")
        return None


def calculate_total_watch_time(df):
    """Calculates total watch time in hours."""
    if df.empty:
        return 0
    total_episodes = df[df['status'] == 'completed']['num_episodes'].sum()
    total_hours = (total_episodes * 24) / 60
    return total_hours


def analyze_genres(df):
    """Analyzes most watched genres."""
    if df.empty:
        return pd.Series([])
    all_genres = []
    for genres in df['genres']:
        all_genres.extend(genres)
    genre_counts = pd.Series(all_genres).value_counts()
    return genre_counts

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        background-color: #f8f9fa; /* Light gray background */
        border: 1px solid #eee;
    }
    .st-emotion-cache-6qob1r {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #eee;
    }
    .st-emotion-cache-10trblm {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #eee;
    }
    .st-emotion-cache-16txtl3 {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #eee;
    }
    .st-emotion-cache-1kyxmqy {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #eee;
    }

    .metric-container {
        background-color: #e9ecef; /* Slightly darker gray for metrics */
        padding: 1rem;
        border-radius: 8px;
        text-align: center; /* Center metric text */
        margin-bottom: 1rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #343a40; /* Darker text color for headings */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("MyAnimeList Dashboard")

username = st.text_input("Enter your MyAnimeList username:", "Matthew9721")
if username:
    with st.spinner("Fetching data..."):
        animelist_df = fetch_user_animelist(username)

    if animelist_df is not None and not animelist_df.empty:

        # --- First Row (Total Watch Time and Average Score) ---
        first_row_cols = st.columns(2)

        with first_row_cols[0]:
            with st.container():
                st.subheader("Total Watch Time")
                total_hours = calculate_total_watch_time(animelist_df)
                st.markdown(
                    f'<div class="metric-container"><h2>{total_hours:.2f}</h2><p>Total Watch Time (Hours)</p></div>',
                    unsafe_allow_html=True)

        with first_row_cols[1]:
            with st.container():
                st.subheader("Average Score")
                scores = animelist_df[animelist_df['score'] > 0]['score']
                if not scores.empty:
                    avg_score = scores.mean()
                    st.markdown(f'<div class="metric-container"><h2>{avg_score:.2f}</h2><p>Average Score</p></div>',
                                unsafe_allow_html=True)
                else:
                    st.info("No scores available to calculate average.")

        # --- Second Row (Genres, Status, Score Distribution) ---
        second_row_cols = st.columns(3)

        with second_row_cols[0]:
            with st.container():
                st.subheader("Most Watched Genres")
                genre_counts = analyze_genres(animelist_df)
                if not genre_counts.empty:
                    fig = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values,
                                 labels={'x': 'Genre', 'y': 'Count'},
                                 color_discrete_sequence=px.colors.qualitative.Prism)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No genre data available.")

        with second_row_cols[1]:
            with st.container():
                st.subheader("Anime Status Counts")
                status_counts = animelist_df['status'].value_counts()
                fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index,
                             color_discrete_sequence=px.colors.qualitative.Pastel1, hole=0.3)
                st.plotly_chart(fig, use_container_width=True)

        with second_row_cols[2]:
            with st.container():
                st.subheader("Score Distribution")
                scores = animelist_df[animelist_df['score'] > 0]['score']
                if not scores.empty:
                    fig_score = px.histogram(scores, nbins=10, labels={'value': 'Score'}, title='Score Distribution',
                                             color_discrete_sequence=px.colors.qualitative.Safe)
                    st.plotly_chart(fig_score, use_container_width=True)
                else:
                    st.info("No scores available.")

        # --- Third Row (Top Rated Anime) ---
        st.subheader("Anime Rated 10/10")
        with st.container():
            top_rated = animelist_df[animelist_df['score'] == 10]
            if not top_rated.empty:
                st.dataframe(top_rated[['title', 'genres', 'status']], use_container_width=True, hide_index=True)
            else:
                st.info("No anime rated 10  /10.")

        # --- Fourth Row (Expandable Data Table) ---
        with st.expander("Show Anime Data"):
            st.dataframe(animelist_df.sort_values(by="score", ascending=False), use_container_width=True, hide_index=True)

    elif animelist_df is not None and animelist_df.empty:
        st.warning(f"The user {username} has no entries in their list.")
    else:
        st.info("Please enter a valid username.")