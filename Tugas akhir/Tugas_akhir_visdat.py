import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    file_path = "McDonald_s_Reviews.csv"  # Ensure the file is in the correct location
    encodings = ['latin1', 'utf-16', 'utf-8-sig']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except Exception:
            continue
    st.error("Failed to load the dataset.")
    return None

data = load_data()

# Title and dataset overview
st.title("McDonald's Reviews Dashboard")

# Add a custom header image 
st.image("McDonalds_Logo.png", use_container_width=True, width=10)

# Refresh the data
data = load_data()

if data is not None:
    # Remove extra spaces in column names
    data.columns = data.columns.str.strip()

    # Dataset Overview
    st.subheader("Dataset Overview")
    st.write(data.head())

    # Clean data for visualization
    data['rating'] = data['rating'].str.extract('(\\d+)').astype(float)
    data['rating_count'] = data['rating_count'].str.replace(',', '').astype(int)

    # 2. Map of McDonald's Locations
    st.subheader("Restaurant Locations")
    fig_map = px.scatter_mapbox(
        data,
        lat='latitude',  # Column name is now stripped of extra spaces
        lon='longitude',
        hover_name='store_address',
        hover_data=['rating'],
        color='rating',
        size='rating_count',
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=3,
        title='McDonald\'s Locations'
    )
    fig_map.update_layout(mapbox_style="open-street-map", title={'x': 0.5})
    st.plotly_chart(fig_map)

    # 3. Word Cloud of Reviews
    st.subheader("Word Cloud of Reviews")
    reviews_text = " ".join(review for review in data['review'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(reviews_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # 4. Rating Distribution
    st.subheader("Rating Distribution")
    fig_rating = px.histogram(
        data,
        x='rating',
        nbins=10,
        title="Distribution of Ratings",
        labels={'rating': 'Rating'},
        color='rating',  # Gunakan 'color' untuk mewarnai batang berdasarkan rating
        template="plotly_dark",  # Gaya Plotly dark theme
    )
    fig_rating.update_layout(
        xaxis_title="Rating",
        yaxis_title="Frequency",
        title={'x': 0.5, 'xanchor': 'center'}
    )
    st.plotly_chart(fig_rating)

    # 5. Top 10 Most Reviewed Locations
    st.subheader("Top 10 Most Reviewed Locations")
    top_locations = data.groupby('store_address').size().reset_index(name='review_count').sort_values(by='review_count', ascending=False).head(10)
    fig_top_locations = px.bar(
        top_locations,
        x='store_address',
        y='review_count',
        title="Top 10 Most Reviewed McDonald's Locations",
        labels={'store_address': 'Store Address', 'review_count': 'Number of Reviews'},
        color='review_count',
        color_continuous_scale='Blues',
        template="plotly_white",  # Gaya Plotly white theme
    )
    fig_top_locations.update_layout(
        xaxis_title="Store Address",
        yaxis_title="Number of Reviews",
        title={'x': 0.5, 'xanchor': 'center'}
    )
    st.plotly_chart(fig_top_locations)

    # 6. Rating Count in Each Location
    st.subheader("Rating Count in Each Location")
    rating_count_per_location = data.groupby('store_address')['rating_count'].sum().reset_index()
    fig_rating_count = px.bar(
        rating_count_per_location,
        x='store_address',
        y='rating_count',
        title="Total Rating Count per McDonald's Location",
        labels={'store_address': 'Store Address', 'rating_count': 'Total Rating Count'},
        color='rating_count',
        color_continuous_scale='YlGnBu',
        template="plotly_dark",  # Gaya Plotly dark theme
    )
    fig_rating_count.update_layout(
        xaxis_title="Store Address",
        yaxis_title="Total Rating Count",
        title={'x': 0.5, 'xanchor': 'center'}
    )
    st.plotly_chart(fig_rating_count)

else:
    st.error("Dataset could not be loaded or is empty.")

