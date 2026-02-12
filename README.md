# 🎶 Song Recommendation System

An interactive **Music Recommendation Web App** built with **Streamlit**.
The app suggests songs based on the selected genre and input song, utilizing content-based filtering techniques.

---

## 🚀 Features

- **Genre Selection**: Choose from popular genres like Bollywood, Tollywood, Kollywood, Sandalwood, Mollywood, English, and Punjabi.
- **Smart Search**: Search for your favorite songs within the selected genre.
- **Personalized Recommendations**: Get top 5 song recommendations based on similarity to your selected track.
- **Spotify Integration**: Play recommended songs directly within the app (via Spotify embed).
- **Rich UI**: Clean, tab-based interface with album art, artist details, and a modern dark-themed design.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NaveenHuggi/song-recommendation.git
   cd song-recommendation
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

   > **Note:** On the first run, the application will automatically download the necessary model files (`songs.pkl` and `similarity.pkl`) from Hugging Face. This may take a few moments depending on your internet connection.

---

## 📂 Project Structure

```
song-recommendation/
├── app.py              # Main Streamlit application logic
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🌍 Live Demo

Check out the live deployment on Streamlit Cloud:
🔗 [Song Recommendation App](https://song-recommendation-a3nvdg8g3k5qbj8ctpuk6t.streamlit.app/)

---

## 📧 Contact

**Author:** Naveen Huggi
📩 Feel free to reach out for collaborations or questions!
