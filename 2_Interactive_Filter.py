import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="IMDb 2024 - Interactive Filter", layout="wide")
st.title("🎯 Advanced Interactive Filtering")

# ----------------------------------------
# ✅ Database Connection (same as main)
# ----------------------------------------
username = 'root'
password = 'root'
hostname = 'localhost'
database = 'DATA_2024'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}/{database}")

# ----------------------------------------
# ✅ Load Data
# ----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM imdb_movies", con=engine)

    # Clean numeric columns
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
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Duration'] = df['Duration'].astype(str).str.extract(r'(\d+)').astype(float)
    df['Main_Genre'] = df['Genre'].astype(str).str.split(',').str[0].str.strip()

    return df

df = load_data()

# ----------------------------------------
# ✅ Sidebar Filters
# ----------------------------------------
st.sidebar.header("Filter Criteria")

# Duration Filter
duration_option = st.sidebar.selectbox(
    "Duration (Hours)",
    ["Any", "< 2 hrs", "2–3 hrs", "> 3 hrs"]
)

# Ratings Filter
min_rating = st.sidebar.slider(
    "Minimum IMDb Rating",
    min_value=0.0, max_value=10.0,
    value=0.0, step=0.1
)

# Votes Filter
min_votes = st.sidebar.number_input(
    "Minimum Votes",
    min_value=0, value=0, step=1000
)

# Genre Filter
genres = df['Main_Genre'].dropna().unique().tolist()
selected_genres = st.sidebar.multiselect(
    "Select Genres",
    options=sorted(genres),
    default=[]
)

# ----------------------------------------
# ✅ Apply Filters
# ----------------------------------------

filtered_df = df.copy()

# Duration: convert to hours filter
if duration_option == "< 2 hrs":
    filtered_df = filtered_df[filtered_df['Duration'] < 120]
elif duration_option == "2–3 hrs":
    filtered_df = filtered_df[(filtered_df['Duration'] >= 120) & (filtered_df['Duration'] <= 180)]
elif duration_option == "> 3 hrs":
    filtered_df = filtered_df[filtered_df['Duration'] > 180]

# Rating filter
filtered_df = filtered_df[filtered_df['Rating'] >= min_rating]

# Votes filter
filtered_df = filtered_df[filtered_df['Votes'] >= min_votes]

# Genre filter
if selected_genres:
    filtered_df = filtered_df[filtered_df['Main_Genre'].isin(selected_genres)]

# ----------------------------------------
# ✅ Show Filtered Results
# ----------------------------------------

st.subheader("Filtered Results")
st.write(f"Showing {len(filtered_df)} movies matching your filters.")

st.dataframe(
    filtered_df[['Title', 'Main_Genre', 'Duration', 'Rating', 'Votes']].sort_values(
        by='Rating', ascending=False
    )
)

