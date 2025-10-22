# ContentMood Analytics 📚☕

A behavioral analytics platform that tracks the correlation between content consumption (books, anime, movies, TV shows) and emotional well-being. Built to understand how different types of media impact mood and emotional states over time.

## 🌟 Project Overview

ContentMood Analytics helps users identify patterns in their content consumption habits and understand which genres, formats, and stories have the most positive impact on their emotional state. The platform combines data tracking, statistical analysis, and interactive visualizations to provide actionable insights.

## 🎯 Key Features

- **Multi-Format Content Tracking**: Log books, anime, movies, and TV shows with detailed metadata
- **Mood Analytics**: Track emotional states before and after consuming content
- **Correlation Analysis**: Identify which content types and genres improve mood the most
- **Interactive Dashboard**: Visualize consumption patterns and mood trends over time
- **Personalized Recommendations**: Get mood-based content suggestions based on historical data
- **Statistical Insights**: Calculate average mood improvements by genre and content type

## 🛠️ Technical Stack

- **Backend**: Python 3.11, SQLite3
- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly
- **Database**: SQLite with normalized schema

## 📊 Database Schema

The application uses a relational database with two main tables:

### Content Table
- Stores title, type, genre, creator, release year, rating, and consumption date
- Tracks user notes and timestamps

### Mood Logs Table
- Records mood before and after consuming content (1-10 scale)
- Captures emotional tags and timestamps
- Foreign key relationship with content table

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/contentmood-analytics.git
cd contentmood-analytics
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize the database**
```bash
python database.py
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### Adding Content
1. Navigate to "Add New Content" page
2. Fill in content details (title, type, genre, etc.)
3. Rate the content (0-10 scale)
4. Log your mood before and after
5. Add emotional tags to track specific feelings

### Viewing Analytics
- **Dashboard**: See recent content and mood trends
- **Analytics**: Explore content breakdown, mood impact by genre, and consumption patterns
- **Insights**: Get personalized recommendations and fun stats

## 📈 Sample Analysis Features

- **Genre Impact Analysis**: Calculate average mood improvement by genre
- **Content Type Comparison**: Compare effectiveness of different media formats
- **Temporal Trends**: Track consumption and mood patterns over time
- **Correlation Studies**: Identify relationships between content attributes and emotional responses

## 💡 Use Cases

- **Personal Development**: Understand which content supports emotional well-being
- **Reading/Viewing Habits**: Track consumption patterns and identify preferences
- **Mood Management**: Find content that reliably improves emotional state
- **Content Discovery**: Get recommendations based on current mood or desired emotional outcome

## 🎨 Design Philosophy

The interface features a soft, bookish aesthetic with cream, brown, and warm earth tones to create a cozy, welcoming experience while maintaining professional data visualization standards.

## 📊 Technical Highlights

- **Normalized database design** with proper foreign key relationships
- **SQL queries** using JOINs, aggregations, and window functions
- **Data validation** and error handling throughout
- **Responsive Streamlit interface** with custom CSS styling
- **Interactive Plotly visualizations** for data exploration
- **Modular code structure** for maintainability

## 🚧 Future Enhancements

- Machine learning model for content recommendations
- Export functionality for data analysis in external tools
- Multi-user support with authentication
- Integration with Goodreads/MyAnimeList APIs
- Advanced statistical analysis (regression, clustering)
- Mobile-responsive design improvements

