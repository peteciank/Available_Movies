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

# Streamlit sidebar
option = st.sidebar.selectbox("Select Option", ["New Releases", "Movies & Series"])

if option == "New Releases":
    url = "https://streaming-availability.p.rapidapi.com/changes"
    querystring = {"item_type": "show", "change_type": "new", "country": "ar", "order_direction": "asc", "include_unknown_dates": "false"}
else:
    url = "https://streaming-availability.p.rapidapi.com/shows/search/filters"
    querystring = {
        "country": "ar",
        "series_granularity": "show",
        "order_by": "original_title",
        "output_language": "en",
        "order_direction": "asc",
        "genres_relation": "and"
    }
    show_type = st.sidebar.selectbox("Select Show Type", ["Movies", "Series"])
    if show_type == "Movies":
        querystring["show_type"] = "movie"
    else:
        querystring["show_type"] = "series"

headers = {
    "X-RapidAPI-Key": "c670840c8fmsh7c24b5f93339517p1475c5jsnb065aa42f09b",
    "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

try:
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()

    shows = data.get("shows", [])

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

    # Displaying titles in columns
    cols = st.columns(3)  # Adjust the number of columns as needed
    for idx, show in enumerate(shows):
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
