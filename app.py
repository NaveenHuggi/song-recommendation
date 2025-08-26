import streamlit as st
import pickle
import pandas as pd
import ast

# --- Background Styling ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    [data-testid="stSidebar"] {
        background-color: rgba(30,30,30,0.85);
    }
    .song-card {
        text-align: center;
        padding: 12px;
        border-radius: 12px;
        background-color: rgba(30,30,30,0.9);
        margin: 10px;
        transition: transform 0.3s, background-color 0.3s;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    }
    .song-card:hover {
        transform: scale(1.05);
        background-color: rgba(40,40,40,0.95);
    }
    img {
        border-radius: 10px;
    }
    .song-title {
        font-size: 16px;
        font-weight: bold;
        margin-top: 8px;
    }
    .song-info {
        font-size: 13px;
        color: #cccccc;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
new_songs = pickle.load(open('songs.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Extract Artist & Genre ---
def extract_info(tags):
    parts = tags.split('[')

    # Extract artist list
    artist_list = []
    if len(parts) > 1:
        artist_str = '[' + parts[1].split(']')[0] + ']'
        try:
            artist_list = ast.literal_eval(artist_str)
        except:
            artist_list = [artist_str]
        artist_list = [artist.title() for artist in artist_list]

    # Extract genre
    genre = parts[-1].split(']')[-1].strip().title()
    return artist_list, genre

# --- Recommender Function ---
def recommend(track_name):
    track_index = new_songs[new_songs['Track Name'] == track_name].index[0]
    distances = similarity[track_index]
    track_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_data = []
    for i in track_list:
        recommended_data.append({
            'Track ID': new_songs.iloc[i[0]]['Track ID'],
            'Track Name': new_songs.iloc[i[0]]['Track Name'],
            'Cover Image': new_songs.iloc[i[0]]['Cover Image'],
            'Tags': new_songs.iloc[i[0]]['Tags']
        })
    return recommended_data

# --- Session State ---
if "playing_track" not in st.session_state:
    st.session_state.playing_track = None
    st.session_state.playing_name = None
if "recommended" not in st.session_state:
    st.session_state.recommended = []

# --- Main UI ---
st.title('🎶 Song Recommender System')

# Step 1: Genre Selection
genres = ['Bollywood', 'Tollywood', 'Kollywood', 'Sandalwood', 'Mollywood', 'English', 'Punjabi']
selected_genre = st.selectbox("🎼 *Select Genre:*", genres)

# Filter songs by genre
filtered_songs = []
for idx, row in new_songs.iterrows():
    _, genre = extract_info(row['Tags'])
    if genre.lower() == selected_genre.lower():
        filtered_songs.append(row['Track Name'])

# Step 2: Song Search
search_query = st.text_input("🔍 Search a song in this genre:")
if search_query:
    filtered_songs = [s for s in filtered_songs if search_query.lower() in s.lower()]

if filtered_songs:
    selected_song = st.selectbox('🎧 *Select a Song:*', filtered_songs)
else:
    selected_song = None
    st.warning("No songs match your search in this genre.")

# Step 3: Show Recommendations
if selected_song and st.button('Recommend'):
    st.session_state.recommended = recommend(selected_song)

tab1, tab2 = st.tabs(["🎵 Recommendations", "📜 Song Details"])

# --- Tab 1: Spotify Embed Layout ---
with tab1:
    if st.session_state.recommended:
        st.subheader("🎶 *Top 5 Recommendations*")
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                song = st.session_state.recommended[i]
                song_name = song['Track Name']
                cover = song['Cover Image']
                track_id = song['Track ID']

                st.markdown(f"""
                    <div class="song-card">
                        <img src="{cover}" width="150">
                        <div class="song-title">{song_name}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Disable other play buttons if another song is playing
                disabled = (
                    st.session_state.playing_track is not None
                    and st.session_state.playing_track != track_id
                )

                # Play button with song name
                if st.button(f"▶️ Play {song_name}", key=f"play_{i}", disabled=disabled):
                    st.session_state.playing_track = track_id
                    st.session_state.playing_name = song_name

        # Now Playing Section
        if st.session_state.playing_track:
            st.markdown("### 🎧 Now Playing")
            st.markdown(f"**{st.session_state.playing_name}**")

            spotify_embed = f"https://open.spotify.com/embed/track/{st.session_state.playing_track}?autoplay=1"

            st.markdown(f"""
                <div style="position:relative; text-align:center;">
                    <iframe src="{spotify_embed}" width="100%" height="352" frameborder="0"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    style="border-radius:12px;"></iframe>
                </div>
            """, unsafe_allow_html=True)

            # Floating Stop Button
            if st.button("⏹ Stop", key="stop_button"):
                st.session_state.playing_track = None
                st.session_state.playing_name = None

# --- Tab 2: Song Details ---
with tab2:
    st.subheader("📜 *Song Details*")
    for song in st.session_state.recommended:
        artist_list, genre = extract_info(song['Tags'])
        st.markdown(f"""
            <div style="background-color:rgba(30,30,30,0.9); padding:15px; border-radius:12px; margin-bottom:15px; text-align:center;">
                <img src="{song['Cover Image']}" width="220" style="border-radius:10px;"><br>
                <b>Song:</b> {song['Track Name']}<br>
                <b>Artists:</b> {', '.join(artist_list)}<br>
                <b>Genre:</b> {genre}
            </div>
        """, unsafe_allow_html=True)
