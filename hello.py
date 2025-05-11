# Import libraries
import pandas as pd
import plotly.express as px
import preswald
from preswald import connect, get_df, table, text, plotly

# Step 1: Load the Dataset
connect()
df = get_df("netflix_titles")

# Step 2: Query or manipulate the data
# (I’m using Pandas instead of SQL because I kept getting a null table with SQL queries. 
# This likely indicates data parsing issues in the backend. 
# Using Pandas is a safer and faster mitigation given the time constraints.)

df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')  # Force 'release_year' to numeric
df = df.dropna(subset=['release_year'])  # Drop rows with invalid or missing 'release_year'
df['release_year'] = df['release_year'].astype(int) 
filtered_df = df[df['release_year'] >= 2015]

# Step 3: Compact the Table
columns_to_keep = ['title', 'type', 'release_year', 'country', 'rating', 'duration']
compact_filtered_df = filtered_df[columns_to_keep]

# Step 4: Build Interactive UI
text("# Netflix Data Explorer ")
text("Browse Netflix titles released after 2015.")
table(compact_filtered_df, title="Netflix Titles After 2015 (Compact View)")

# Step 5: Create and Display a Visualization
# Group number of titles by release year and type
titles_per_year = df.groupby(['release_year', 'type']).size().reset_index(name='count')

# Scatter plot: Titles Released Per Year, colored by Type (Movie/TV Show)
fig = px.scatter(
    titles_per_year,
    x="release_year",
    y="count",
    color="type",
    title="Netflix Titles Released Per Year by Type",
    labels={
        "release_year": "Release Year",
        "count": "Number of Titles",
        "type": "Content Type"
    }
)

fig.update_layout(template="plotly_white")

plotly(fig)