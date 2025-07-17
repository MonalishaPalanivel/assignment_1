import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# ----------------------------------------
# ✅ Streamlit Page Config
# ----------------------------------------
st.set_page_config(page_title="IMDb 2024 Dashboard", layout="wide")
st.title("🎬 IMDb 2024 Interactive Dashboard")

# ----------------------------------------
# ✅ Database Connection
# ----------------------------------------
username = 'root'
password = 'root'
hostname = 'localhost'
database = 'DATA_2024'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}/{database}")

# ----------------------------------------
# ✅ Load and Clean Data
# ----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM imdb_movies", con=engine)

    # Parse Votes: handle k, M, commas
    def parse_votes(v):
        if pd.isnull(v):
            return 0
        v = str(v).lower().strip().replace(',', '')
        if v.endswith('k'):
            return float(v[:-1]) * 1_000
        elif v.endswith('m'):
            return float(v[:-1]) * 1_000_000
        else:
            try:
                return float(v)
            except:
                return 0

    df['Votes'] = df['Votes'].apply(parse_votes)

    # Parse Rating safely
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Parse Duration: if your scraped data has "120 min" or similar
    df['Duration'] = df['Duration'].astype(str).str.extract(r'(\d+)').astype(float)

    # If Genre has multiple, take first
    df['Main_Genre'] = df['Genre'].astype(str).str.split(',').str[0].str.strip()

    return df

df = load_data()

# ----------------------------------------
# ✅ Sidebar: Minimum Votes Filter
# ----------------------------------------
st.sidebar.header("Filters")
min_votes = st.sidebar.number_input(
    "Minimum Votes for Top Rated Movies",
    value=1000,
    min_value=0,
    step=100
)

# ----------------------------------------
# ✅ 1️⃣ Top 10 by Rating & Voting Counts
# ----------------------------------------
st.header("1️⃣ Top 10 Movies by Rating & Voting Counts")

# Top 10 by Rating
top_by_rating = df[df['Votes'] >= min_votes].sort_values(
    by='Rating', ascending=False
).head(10)

fig_rating = px.bar(
    top_by_rating,
    x='Title',
    y='Rating',
    color='Rating',
    text='Rating',
    hover_data=['Votes'],
    title=f'Top 10 Highest Rated Movies (Min {min_votes} Votes)'
)
fig_rating.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_rating, use_container_width=True)

# Top 10 by Votes
top_by_votes = df.sort_values(by='Votes', ascending=False).head(10)

fig_votes = px.bar(
    top_by_votes,
    x='Title',
    y='Votes',
    color='Votes',
    text='Votes',
    hover_data=['Rating'],
    title='Top 10 Most Voted Movies'
)
fig_votes.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_votes, use_container_width=True)

# ----------------------------------------
# ✅ 2️⃣ Genre Distribution
# ----------------------------------------
st.header("2️⃣ Genre Distribution")
genre_counts = df['Main_Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']

fig_genre_dist = px.bar(
    genre_counts,
    x='Genre',
    y='Count',
    color='Count',
    title='Number of Movies per Genre'
)
st.plotly_chart(fig_genre_dist, use_container_width=True)

# ----------------------------------------
# ✅ 3️⃣ Average Duration by Genre
# ----------------------------------------
st.header("3️⃣ Average Duration by Genre")
avg_duration = df.groupby('Main_Genre')['Duration'].mean().reset_index().dropna()

fig_avg_duration = px.bar(
    avg_duration,
    x='Duration',
    y='Main_Genre',
    orientation='h',
    color='Duration',
    title='Average Movie Duration by Genre'
)
st.plotly_chart(fig_avg_duration, use_container_width=True)

# ----------------------------------------
# ✅ 4️⃣ Voting Trends by Genre
# ----------------------------------------
st.header("4️⃣ Average Voting Counts by Genre")
avg_votes = df.groupby('Main_Genre')['Votes'].mean().reset_index().dropna()

fig_avg_votes = px.bar(
    avg_votes,
    x='Main_Genre',
    y='Votes',
    color='Votes',
    title='Average Votes per Genre'
)
st.plotly_chart(fig_avg_votes, use_container_width=True)

# ----------------------------------------
# ✅ 5️⃣ Rating Distribution
# ----------------------------------------
st.header("5️⃣ Rating Distribution")
fig_hist = px.histogram(df, x='Rating', nbins=20, title='Histogram of Ratings')
st.plotly_chart(fig_hist, use_container_width=True)

fig_box = px.box(df, y='Rating', title='Boxplot of Ratings')
st.plotly_chart(fig_box, use_container_width=True)

# ----------------------------------------
# ✅ 6️⃣ Genre-Based Rating Leaders
# ----------------------------------------
st.header("6️⃣ Top-Rated Movie per Genre")
leaders = df.loc[df.groupby('Main_Genre')['Rating'].idxmax()][['Main_Genre', 'Title', 'Rating', 'Votes']]
st.dataframe(leaders)

# ----------------------------------------
# ✅ 7️⃣ Most Popular Genres by Voting
# ----------------------------------------
st.header("7️⃣ Most Popular Genres by Total Votes")
votes_by_genre = df.groupby('Main_Genre')['Votes'].sum().reset_index().dropna()

fig_pie = px.pie(
    votes_by_genre,
    names='Main_Genre',
    values='Votes',
    title='Genres with Highest Total Votes'
)
st.plotly_chart(fig_pie, use_container_width=True)

# ----------------------------------------
# ✅ 8️⃣ Duration Extremes
# ----------------------------------------
st.header("8️⃣ Shortest & Longest Movies")

shortest = df[df['Duration'].notnull()].sort_values('Duration').head(1)
longest = df[df['Duration'].notnull()].sort_values('Duration', ascending=False).head(1)

col1, col2 = st.columns(2)
with col1:
    if not shortest.empty:
        st.metric("🎬 Shortest Movie", f"{shortest.iloc[0]['Title']} ({shortest.iloc[0]['Duration']} mins)")
    else:
        st.warning("No valid duration data for shortest movie.")

with col2:
    if not longest.empty:
        st.metric("🎥 Longest Movie", f"{longest.iloc[0]['Title']} ({longest.iloc[0]['Duration']} mins)")
    else:
        st.warning("No valid duration data for longest movie.")

# ----------------------------------------
# ✅ 9️⃣ Ratings by Genre (Heatmap)
# ----------------------------------------
st.header("9️⃣ Ratings by Genre (Heatmap)")
avg_rating_by_genre = df.groupby('Main_Genre')['Rating'].mean().reset_index()

fig_heatmap = px.density_heatmap(
    avg_rating_by_genre,
    x='Main_Genre',
    y='Rating',
    nbinsx=len(avg_rating_by_genre),
    title='Average Ratings by Genre',
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ----------------------------------------
# ✅ 🔟 Correlation Analysis: Ratings vs Votes
# ----------------------------------------
st.header("🔟 Correlation: Ratings vs Votes")
fig_scatter = px.scatter(
    df,
    x='Votes',
    y='Rating',
    trendline='ols',
    title='Correlation between Votes and Ratings',
    hover_data=['Title', 'Main_Genre']
)
st.plotly_chart(fig_scatter, use_container_width=True)

