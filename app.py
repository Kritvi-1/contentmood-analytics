import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import ContentDatabase

# Page configuration
st.set_page_config(
    page_title="ContentMood Analytics ☕📚",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# COMPLETELY FIXED CSS
st.markdown("""
    <style>
    /* Force light theme */
    .stApp {
        background-color: #FAF6F0 !important;
    }
    
    .main .block-container {
        background-color: #FAF6F0 !important;
        padding-top: 2rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #E8D5C4 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #E8D5C4 !important;
    }
    
    /* All text brown */
    h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
        color: #6B5444 !important;
        font-family: 'Georgia', serif !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #8B7355 !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6B5444 !important;
    }
    
    /* Buttons with hover */
    .stButton > button {
        background-color: #A0826D !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(107, 84, 68, 0.2) !important;
    }
    
    .stButton > button:hover {
        background-color: #8B7355 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(107, 84, 68, 0.3) !important;
    }
    
    /* ALL TEXT INPUTS - BEIGE with BROWN text */
    input[type="text"], 
    input[type="number"],
    input[type="date"],
    textarea,
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stDateInput input {
        background-color: #F5EFE6 !important;
        border: 2px solid #D4A574 !important;
        border-radius: 8px !important;
        color: #6B5444 !important;
        padding: 8px !important;
    }
    
    /* Force placeholder and actual text to be brown */
    input::placeholder, textarea::placeholder {
        color: #A0826D !important;
        opacity: 0.7 !important;
    }
    
    /* Hover effects on inputs */
    input:hover, textarea:hover {
        border-color: #A0826D !important;
        box-shadow: 0 2px 4px rgba(160, 130, 109, 0.2) !important;
    }
    
    input:focus, textarea:focus {
        border-color: #8B7355 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(160, 130, 109, 0.25) !important;
    }
    
    /* Selectbox - BEIGE with hover */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] div[role="button"] {
        background-color: #F5EFE6 !important;
        border: 2px solid #D4A574 !important;
        border-radius: 8px !important;
        color: #6B5444 !important;
        transition: all 0.2s ease !important;
    }
    
    [data-baseweb="select"]:hover > div {
        border-color: #A0826D !important;
        box-shadow: 0 2px 4px rgba(160, 130, 109, 0.2) !important;
    }
    
    [data-baseweb="select"] span {
        color: #6B5444 !important;
    }
    
    /* Dropdown menu */
    [data-baseweb="popover"] {
        background-color: #F5EFE6 !important;
    }
    
    [role="listbox"] {
        background-color: #F5EFE6 !important;
        border: 2px solid #D4A574 !important;
    }
    
    [role="option"] {
        background-color: #F5EFE6 !important;
        color: #6B5444 !important;
    }
    
    [role="option"]:hover {
        background-color: #E8D5C4 !important;
    }
    
    [aria-selected="true"] {
        background-color: #E8D5C4 !important;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] {
        color: #6B5444 !important;
    }
    
    /* Content cards - nice boxes for recent items */
    .content-card {
        background-color: #F5EFE6 !important;
        border: 2px solid #D4A574 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .content-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 6px 12px rgba(107, 84, 68, 0.2) !important;
        border-color: #A0826D !important;
    }
    
    /* Tabs with hover */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #E8D5C4 !important;
        color: #6B5444 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #D4A574 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #A0826D !important;
        color: white !important;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        background-color: #F5EFE6 !important;
        border: 2px solid #D4A574 !important;
        color: #6B5444 !important;
    }
    
    /* Hide toolbar */
    [data-testid="stToolbar"] {
        display: none;
    }
    
    footer {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper functions
def get_mood_emoji(mood_score):
    if mood_score <= 3:
        return "😢"
    elif mood_score <= 5:
        return "😐"
    elif mood_score <= 7:
        return "🙂"
    else:
        return "😊"

def get_content_icon(content_type):
    icons = {
        "Book": "📚",
        "Movie": "🎬",
        "TV Show": "📺",
        "Anime": "🎌",
        "Manga": "📖",
        "Game": "🎮",
        "Podcast": "🎙️"
    }
    return icons.get(content_type, "📌")

# Initialize database
db = ContentDatabase()

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 📚 ContentMood Analytics")
    st.markdown("*Track your emotional journey through stories*")
    st.markdown("---")
    
    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "➕ Add New Content", "📊 Analytics", "💡 Insights"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    
    # Get quick stats
    content_df = db.get_all_content()
    mood_df = db.get_content_with_moods()
    
    if not content_df.empty:
        st.metric("Total Content", len(content_df))
        
        if not mood_df.empty and 'mood_change' in mood_df.columns:
            avg_mood_boost = mood_df['mood_change'].mean()
            st.metric("Avg Mood Boost", f"+{avg_mood_boost:.1f}")
    
   
# Main Content Area
if page == "🏠 Dashboard":
    st.title("📚 Welcome to Your Reading Journey")
    
    if content_df.empty:
        st.info("👋 Start by adding your first book, show, or anime!")
    else:
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Content", len(content_df))
        
        with col2:
            books_count = len(content_df[content_df['content_type'] == 'Book'])
            st.metric("📖 Books Read", books_count)
        
        with col3:
            anime_count = len(content_df[content_df['content_type'] == 'Anime'])
            st.metric("🎌 Anime Watched", anime_count)
        
        with col4:
            avg_rating = content_df['rating'].mean()
            st.metric("⭐ Avg Rating", f"{avg_rating:.1f}/10")
        
        st.markdown("---")
        
        # Recently consumed content
        st.subheader("☀️ Recently Consumed")
        recent = content_df.head(6)
        
        cols = st.columns(3)
        for idx, (_, row) in enumerate(recent.iterrows()):
            with cols[idx % 3]:
                # Create a card with hover effect
                st.markdown(f"""
                <div class="content-card">
                    <h3 style="color: #6B5444; margin-top: 0;">{get_content_icon(row['content_type'])} {row['title']}</h3>
                    <p style="color: #8B7355; font-weight: 600; margin: 8px 0;">{row['genre']}</p>
                    <p style="color: #A0826D; margin: 8px 0;">{'⭐' * int(row['rating'])} {row['rating']}/10</p>
                    <p style="color: #6B5444; font-style: italic; font-size: 14px; margin: 8px 0;">
                        {row['notes'][:60] + '...' if pd.notna(row['notes']) and len(str(row['notes'])) > 60 else (row['notes'] if pd.notna(row['notes']) else '')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Mood Journey
        st.subheader("📈 Your Mood Journey")
        
        if not mood_df.empty and 'mood_after' in mood_df.columns:
            mood_df['date_consumed'] = pd.to_datetime(mood_df['date_consumed'])
            mood_df_sorted = mood_df.sort_values('date_consumed')
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=mood_df_sorted['date_consumed'],
                y=mood_df_sorted['mood_after'],
                name='Mood After',
                line=dict(color='#8B7355', width=3),
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(139, 115, 85, 0.2)'
            ))
            
            fig.add_trace(go.Scatter(
                x=mood_df_sorted['date_consumed'],
                y=mood_df_sorted['mood_before'],
                name='Mood Before',
                line=dict(color='#D4A574', dash='dash', width=2),
                mode='lines'
            ))
            
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='#FAF6F0',
                font=dict(color='#6B5444', family='Georgia', size=12),
                xaxis_title="Date",
                yaxis_title="Mood Score",
                yaxis=dict(
                    range=[0, 11], 
                    gridcolor='#E8D5C4', 
                    tickfont=dict(color='#6B5444'),
                    title_font=dict(color='#6B5444')
                ),
                xaxis=dict(
                    gridcolor='#E8D5C4', 
                    tickfont=dict(color='#6B5444'),
                    title_font=dict(color='#6B5444')
                ),
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(color='#6B5444')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add mood tracking to see your emotional journey!")

elif page == "➕ Add New Content":
    st.title("➕ Add New Content")
    st.markdown("*Log what you've been reading, watching, or experiencing*")
    
    with st.form("add_content_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📚 Title *")
            content_type = st.selectbox(
                "📁 Content Type *",
                ["Book", "Movie", "TV Show", "Anime", "Manga", "Game", "Podcast"]
            )
            genre = st.text_input("🎭 Genre")
            creator = st.text_input("✍️ Creator/Author")
        
        with col2:
            release_year = st.number_input("📅 Release Year", min_value=1900, max_value=2025, value=2024)
            date_consumed = st.date_input("📆 Date Consumed *", value=datetime.now())
            rating = st.slider("⭐ Your Rating", 0.0, 10.0, 5.0, 0.5)
            notes = st.text_area("📝 Notes", placeholder="What did you think? How did it make you feel?")
        
        st.markdown("---")
        st.markdown("**🎭 Mood Tracking**")
        
        mood_options = {
            "😢 Very Sad (1-2)": 1.5,
            "😔 Sad (3-4)": 3.5,
            "😐 Neutral (5-6)": 5.5,
            "🙂 Happy (7-8)": 7.5,
            "😊 Very Happy (9-10)": 9.5
        }
        
        col3, col4 = st.columns(2)
        
        with col3:
            mood_before_option = st.selectbox(
                "😐 Mood Before",
                options=list(mood_options.keys()),
                index=2
            )
            mood_before = mood_options[mood_before_option]
        
        with col4:
            mood_after_option = st.selectbox(
                "😊 Mood After", 
                options=list(mood_options.keys()),
                index=3
            )
            mood_after = mood_options[mood_after_option]
        
        emotional_tags = st.text_input(
            "💭 Emotional Tags",
            placeholder="happy, sad, excited, inspired..."
        )
        
        submitted = st.form_submit_button("✨ Add to Collection")
        
        if submitted:
            if title:
                content_id = db.add_content(
                    title=title,
                    content_type=content_type,
                    genre=genre,
                    creator=creator,
                    release_year=release_year,
                    date_consumed=date_consumed.strftime('%Y-%m-%d'),
                    rating=rating,
                    notes=notes
                )
                
                db.add_mood_log(
                    content_id=content_id,
                    mood_before=int(mood_before),
                    mood_after=int(mood_after),
                    emotional_tags=emotional_tags,
                    log_date=date_consumed.strftime('%Y-%m-%d')
                )
                
                st.success(f"✨ {title} added successfully!")
                st.snow()  # Falling pages effect!
                st.markdown("✨📚☕ *Added to your collection!*")
            else:
                st.error("Please fill in the required fields (Title)")

elif page == "📊 Analytics":
    st.title("📊 Analytics")
    st.markdown("*Dive deep into your consumption patterns*")
    
    if content_df.empty:
        st.info("No data yet! Start adding content to see analytics.")
    else:
        tab1, tab2, tab3 = st.tabs(["📚 Content Breakdown", "🎭 Mood Analysis", "📈 Trends"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Content Types")
                type_counts = content_df['content_type'].value_counts()
                fig1 = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    color_discrete_sequence=['#A0826D', '#D4A574', '#8B7355', '#E8D5C4', '#B8956A']
                )
                fig1.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='#FAF6F0',
                    font=dict(color='#6B5444', family='Georgia', size=14),
                    title_font=dict(color='#6B5444')
                )
                fig1.update_traces(
                    textfont=dict(color='#6B5444', size=13),
                    marker=dict(line=dict(color='#6B5444', width=1))
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.subheader("Top Genres")
                genre_counts = content_df['genre'].value_counts().head(10)
                fig2 = px.bar(
                    x=genre_counts.values,
                    y=genre_counts.index,
                    orientation='h',
                    color_discrete_sequence=['#A0826D']
                )
                fig2.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='#FAF6F0',
                    font=dict(color='#6B5444', family='Georgia', size=12),
                    xaxis_title="Count",
                    yaxis_title="Genre",
                    showlegend=False,
                    xaxis=dict(
                        gridcolor='#E8D5C4', 
                        tickfont=dict(color='#6B5444'),
                        title_font=dict(color='#6B5444')
                    ),
                    yaxis=dict(
                        tickfont=dict(color='#6B5444'),
                        title_font=dict(color='#6B5444')
                    )
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            st.subheader("⭐ Ratings Distribution")
            fig3 = px.histogram(
                content_df,
                x='rating',
                nbins=20,
                color_discrete_sequence=['#A0826D']
            )
            fig3.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='#FAF6F0',
                font=dict(color='#6B5444', family='Georgia', size=12),
                xaxis_title="Rating",
                yaxis_title="Count",
                xaxis=dict(
                    gridcolor='#E8D5C4', 
                    tickfont=dict(color='#6B5444'),
                    title_font=dict(color='#6B5444')
                ),
                yaxis=dict(
                    gridcolor='#E8D5C4', 
                    tickfont=dict(color='#6B5444'),
                    title_font=dict(color='#6B5444')
                )
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab2:
            if not mood_df.empty and 'mood_change' in mood_df.columns:
                st.subheader("🎭 Mood Impact by Genre")
                
                genre_mood = mood_df.groupby('genre')['mood_change'].mean().sort_values(ascending=False).head(10)
                
                fig4 = px.bar(
                    x=genre_mood.index,
                    y=genre_mood.values,
                    color=genre_mood.values,
                    color_continuous_scale=['#D4A574', '#A0826D', '#8B7355']
                )
                fig4.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='#FAF6F0',
                    font=dict(color='#6B5444', family='Georgia', size=12),
                    xaxis_title="Genre",
                    yaxis_title="Average Mood Change",
                    showlegend=False,
                    xaxis=dict(
                        tickfont=dict(color='#6B5444'),
                        title_font=dict(color='#6B5444')
                    ),
                    yaxis=dict(
                        gridcolor='#E8D5C4', 
                        tickfont=dict(color='#6B5444'),
                        title_font=dict(color='#6B5444')
                    )
                )
                st.plotly_chart(fig4, use_container_width=True)
                
                st.subheader("✨ Top Mood Boosters")
                top_boosters = mood_df.nlargest(5, 'mood_change')[['title', 'content_type', 'mood_change', 'emotional_tags']]
                for _, row in top_boosters.iterrows():
                    with st.container():
                        st.markdown(f"**{get_content_icon(row['content_type'])} {row['title']}**")
                        st.markdown(f"Mood boost: +{row['mood_change']:.1f}")
                        if pd.notna(row['emotional_tags']):
                            st.markdown(f"*Tags: {row['emotional_tags']}*")
                        st.markdown("---")
            else:
                st.info("Add mood tracking data to see mood analysis!")
        
        with tab3:
            st.subheader("📅 Consumption Over Time")
            
            content_df['date_consumed'] = pd.to_datetime(content_df['date_consumed'])
            content_df['month'] = content_df['date_consumed'].dt.to_period('M').astype(str)
            
            monthly_counts = content_df.groupby('month').size().reset_index(name='count')
            
            fig5 = px.line(
                monthly_counts,
                x='month',
                y='count',
                markers=True,
                color_discrete_sequence=['#A0826D']
            )
            fig5.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='#FAF6F0',
                font=dict(color='#6B5444', family='Georgia', size=12),
                xaxis_title="Month",
                yaxis_title="Content Consumed",
                xaxis=dict(
                    tickfont=dict(color='#6B5444'),
                    title_font=dict(color='#6B5444')
                ),
                yaxis=dict(
                    gridcolor='#E8D5C4', 
                    tickfont=dict(color='#6B5444'),
                    title_font=dict(color='#6B5444')
                )
            )
            st.plotly_chart(fig5, use_container_width=True)

elif page == "💡 Insights":
    st.title("💡 Personalized Insights")
    st.markdown("*What do your reading habits reveal about you?*")
    
    if content_df.empty or mood_df.empty:
        st.info("Add more content with mood tracking to unlock personalized insights!")
    else:
        st.subheader("☀️ What Makes You Happiest?")
        
        if not mood_df.empty and 'mood_change' in mood_df.columns:
            best_genre = mood_df.groupby('genre')['mood_change'].mean().idxmax()
            best_genre_boost = mood_df.groupby('genre')['mood_change'].mean().max()
            
            st.markdown(f"""
            <div style='background-color: #F5EFE6; padding: 20px; border-radius: 10px; border: 2px solid #D4A574;'>
                <h3 style='color: #6B5444;'>✨ Your Happy Place: {best_genre}</h3>
                <p style='color: #6B5444;'>This genre consistently boosts your mood by <strong>+{best_genre_boost:.1f} points</strong> on average!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.subheader("📚 Mood-Based Recommendations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 😔 Feeling Down?")
                top_uplifters = mood_df.nlargest(3, 'mood_change')
                for _, row in top_uplifters.iterrows():
                    st.markdown(f"**{get_content_icon(row['content_type'])} {row['title']}**")
                    st.markdown(f"*Mood boost: +{row['mood_change']:.1f}*")
                    st.markdown("")
            
            with col2:
                st.markdown("### 😭 Want Something Emotional?")
                emotional_content = mood_df[mood_df['emotional_tags'].str.contains('sad|crying|emotional', case=False, na=False)].head(3)
                for _, row in emotional_content.iterrows():
                    st.markdown(f"**{get_content_icon(row['content_type'])} {row['title']}**")
                    if pd.notna(row['emotional_tags']):
                        st.markdown(f"*Tags: {row['emotional_tags']}*")
                    st.markdown("")
            
            st.markdown("---")
            
            st.subheader("🎉 Fun Stats About You")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_consumed = len(content_df)
                st.metric("💪 Total Consumed", total_consumed)
                st.markdown("*You're building quite the collection!*")
            
            with col2:
                if not mood_df.empty and 'mood_change' in mood_df.columns:
                    total_mood_boost = mood_df['mood_change'].sum()
                    st.metric("✨ Total Mood Boost", f"+{total_mood_boost:.1f}")
                    st.markdown("*Stories have lifted your spirits!*")
            
            with col3:
                avg_rating = content_df['rating'].mean()
                if avg_rating >= 8:
                    rating_text = "Generous Rater"
                elif avg_rating >= 6:
                    rating_text = "Balanced Critic"
                else:
                    rating_text = "Tough Critic"
                st.metric("⭐ You're a", rating_text)
                st.markdown(f"*Avg rating: {avg_rating:.1f}/10*")

st.markdown("---")
st.markdown("*Made with ☕ and 📚 for book lovers everywhere*")