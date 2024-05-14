import streamlit as st
import requests

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


# For movies and series
url = "https://streaming-availability.p.rapidapi.com/shows/search/filters"

querystring = {
    "country": "ar",
    "show_type": "series",
    "series_granularity": "show",
    "order_by": "original_title",
    "output_language": "en",
    "order_direction": "asc",
    "genres_relation": "and"
}

# For new Releases
#url = "https://streaming-availability.p.rapidapi.com/changes"

#querystring = {"item_type":"show","change_type":"new","country":"ar","order_direction":"asc","include_unknown_dates":"false"}

headers = {
    "X-RapidAPI-Key": "c670840c8fmsh7c24b5f93339517p1475c5jsnb065aa42f09b",
    "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

# Define streaming providers
streaming_providers = {
    "Netflix": "netflix",
    "Amazon Prime Video": "prime",
    "Disney+": "disney",
    "HBO Max": "hbo",
    "Hulu": "hulu",
    "Peacock": "peacock",
    "Paramount+": "paramount",
    "Starz": "starz",
    "Showtime": "showtime",
    "Apple TV+": "apple",
    "Mubi": "mubi",
    "Stan": "stan",
    "Now": "now",
    "Crave": "crave",
    "All 4": "all4",
    "BBC iPlayer": "iplayer",
    "BritBox": "britbox",
    "Hotstar": "hotstar",
    "Zee5": "zee5",
    "Curiosity Stream": "curiosity",
    "Wow": "wow"
}

ShowTypes = {
    "Movies": "movies",
    "Series": "series",
}

# Streamlit sidebar
selected_providers = st.sidebar.multiselect("Select Streaming Providers", list(streaming_providers.keys()))

# Add selected providers to the query parameters
selected_providers_ids = [streaming_providers[provider] for provider in selected_providers]

if selected_providers_ids:
    querystring["providers"] = ",".join(selected_providers_ids)

try:
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()



    with st.expander("Raw Data", expanded=False):

        st.write(data)

    shows = data.get("shows", [])
    st.write(len(shows))
    filtered_shows = []



    for show in shows:
        streaming_options = show.get("streamingOptions", {}).get("ar", [])
        available_providers = [option.get("service", {}).get("id") for option in streaming_options]

        if set(selected_providers_ids).intersection(available_providers):
            filtered_shows.append(show)

    # Styling for the main content
    st.markdown(
        """
        <style>
        .content {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: flex-start;
            align-items: flex-start;
        }
        .title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .description {
            margin-bottom: 10px;
        }
        .poster {
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .streaming-link {
            color: #0066FF;
            text-decoration: none;
            font-weight: bold;
        }
        .streaming-link:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Pagination
    items_per_page = 9
    total_items = len(filtered_shows)
    num_pages = (total_items + items_per_page - 1) // items_per_page
    page = st.sidebar.number_input("Page", min_value=1, max_value=num_pages, value=1)

    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    paginated_shows = filtered_shows[start_idx:end_idx]

    # Displaying titles in columns
    cols = st.columns(3)  # Adjust the number of columns as needed
    for idx, show in enumerate(paginated_shows):
        with cols[idx % 3]:
            with st.container(border=True):
                title = show.get("title")
                description = show.get("overview")
                poster = show.get("imageSet", {}).get("verticalPoster", {}).get("w240")
                streaming_options = show.get("streamingOptions", {}).get("ar", [])

                if title and description and poster and streaming_options:
                    st.markdown(f'<p class="title">{title}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="description">{description}</p>', unsafe_allow_html=True)
                    st.image(poster, caption="Poster", width=150, use_column_width=False, clamp=True, output_format="JPEG")  # Set custom width for the poster

                    st.write("Streaming Options:")
                    for option in streaming_options:
                        service_name = option.get("service", {}).get("name")
                        link = option.get("link")
                        st.markdown(f'<a href="{link}" class="streaming-link" target="_blank">{service_name}</a>', unsafe_allow_html=True)

                    st.write("")

    st.write(f"Page {page}/{num_pages}")

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")

# Adjust Streamlit layout width
st.markdown(
    """
    <style>
    .reportview-container {
        max-width: 90%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
