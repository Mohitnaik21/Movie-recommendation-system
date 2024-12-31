# 🎥 Movie Recommendation System 🍿

A full-stack movie recommendation system with integrated sentiment analysis. This project uses a hybrid recommendation approach, combining collaborative filtering, content-based filtering, and hybrid filtering. It is built with Flask for the backend, 🖌️ Bootstrap for frontend styling, and integrates with The Movie Database (TMDb) API for movie data. 🎬

---

## ✨ Features

### 👤 User Management
- 📝 User registration and login with secure password hashing.
- 📋 Dashboard with personalized recommendations and favorites.

### 🔮 Recommendations
- **🤝 Collaborative Filtering**: Suggests movies based on other users with similar tastes.
- **🔍 Content-Based Filtering**: Recommends movies similar to those the user likes based on genres, directors, and cast.
- **🧠 Hybrid Recommendations**: Combines collaborative and content-based filtering for enhanced suggestions.

### 🧾 Sentiment Analysis
- 🗨️ User reviews are analyzed for sentiment (positive, negative, neutral).
- 📊 Display aggregate sentiment analysis for movies.

### 🌐 TMDb Integration
- 🌟 Fetch real-time movie data such as posters, trailers, and overviews from the TMDb API.
- 🚀 Fetch trending movies and movie-specific details dynamically.

### 🖥️ Responsive Design
- 📱 Fully responsive UI built with Bootstrap.
- 🔗 Seamless navigation between the dashboard, recommendations, and movie details.

---

## 🛠️ Technologies Used

### 🔙 Backend
- 🐍 Flask
- 📦 Flask-SQLAlchemy
- 🔑 Flask-Login

### 🎨 Frontend
- 🖼️ HTML, CSS, Bootstrap
- ⚡ JavaScript for interactivity

### 🧠 Machine Learning
- 🤝 Collaborative filtering with cosine similarity.
- 🧪 Sentiment analysis using NLTK and pre-trained models.

### 🔌 APIs
- 🎬 TMDb API for movie data.

### 📂 Database
- 💾 SQLite (default, easily replaceable with PostgreSQL or MySQL for production).

---

## ⚙️ Installation and Setup

### 📝 Prerequisites
- 🐍 Python 3.8+
- 📦 Virtual environment (optional but recommended)
- 🔑 TMDb API key

### 🔧 Steps
1. **📂 Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **🌐 Set Up a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **📥 Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **🔑 Set Up Environment Variables**:
   Create a `.env` file in the root directory:
   ```plaintext
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///database.db
   TMDB_API_KEY=your_tmdb_api_key
   ```

5. **▶️ Run the Application**:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000`.

---

## 🗂️ Project Structure
## Project Structure
```
.
├── app.py                          # 🚀 Main Flask application
├── models.py                       # 🗄️ Database models
├── routes.py                       # 🛤️ Application routes
├── utils/                          # 🛠️ Utility functions
│   ├── collaborative_filtering.py  # 🤝 Implements collaborative filtering using user similarities.
│   ├── content_based_filtering.py  # 🔍 Recommends movies based on genres, cast, and director.
│   ├── hybrid_recommendation.py    # 🧠 Combines collaborative and content-based filtering for hybrid recommendations. 
│   ├── sentiment_analysis.py       # 🧮 Orchestrates multiple recommendation algorithms to provide ranked suggestions. 
│   ├── recommendation_engine.py    # 🗨️ Analyzes sentiment of user reviews using NLTK.
│   ├── tmdb_api.py                 # 🌐 Handles interactions with TMDb API for movie data retrieval
├── templates/                      # 🖼️ HTML templates
│   ├── index.html                  # 🎬 Homepage
│   ├── dashboard.html              # 🖥️ User Dashboard
│   ├── recommendations.html        # 📊 Recommendations page
│   ├── movie_details.html          # 🎥 Movie details
│   ├── login.html                  # 🔓 Login
│   ├── register.html               # ✍️ Registration
│   ├── search_result.html          # 🔍 Search
├── static/                         # 🎨 Static assets (CSS, JS, images)
├── ├── css/                        # ✒️ Stylesheets
│   │   ├── dashboard.css           # 🖥️ User Dashboard CSS
│   │   ├── recommendations.css     # 📊 Recommendations page CSS
│   │   ├── movie_details.css       # 🎥 Movie details CSS
│   │   ├── styles.css              # 🎬 Homepage CSS
├── requirements.txt                # 📜 Python dependencies
├── .env                            # 🔑 Environment variables (ignored in Git)
└── README.md                       # 📖 Project documentation
```
---

## 🚀 Usage

1. **👤 Register**: Create a new user account.
2. **🔓 Login**: Log in to access personalized recommendations.
3. **📋 Dashboard**:
   - View favorite movies.
   - See trending and recommended movies.
4. **🔍 Search**: Search for movies by title.
5. **📝 Add Reviews**: Submit reviews and view sentiment analysis.

---

## 🌟 Future Enhancements
- 🤖 Incorporate deep learning models for advanced recommendations.
- 🌎 Support multi-language sentiment analysis.
- ⚙️ Add user settings to customize recommendation preferences.
- 🔌 Integrate with additional APIs for more data sources.

---

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

---

## 🙏 Acknowledgments
- 🎬 [TMDb API](https://www.themoviedb.org/documentation/api) for movie data.
- 🖌️ [Bootstrap](https://getbootstrap.com/) for frontend styling.
- 💡 Flask community for their amazing resources and support.

---

🎉 Enjoy exploring movies and sharing your reviews! Feel free to reach out for any suggestions or queries.

