import os
import streamlit as st
import serpapi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")

# Page configuration
st.set_page_config(
    page_title="ScholarWise",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("🎓 ScholarWise")
st.subheader("AI Research Assistant for Students")

st.write(
    "Search academic research papers using Google Scholar "
    "through SerpApi."
)

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("🔎 Search Settings")

year = st.sidebar.selectbox(
    "Publication Year",
    [
        "Any Year",
        "Since 2026",
        "Since 2025",
        "Since 2024",
        "Since 2023",
        "Since 2022"
    ]
)

sort_option = st.sidebar.selectbox(
    "Sort Results",
    [
        "Relevance",
        "Newest"
    ]
)

# -----------------------------
# SEARCH BOX
# -----------------------------

query = st.text_input(
    "🔍 Enter your research topic",
    placeholder="Example: Artificial Intelligence in Healthcare"
)

search_button = st.button(
    "🚀 Search Research Papers",
    type="primary"
)

# -----------------------------
# SEARCH FUNCTION
# -----------------------------

def search_scholar(search_query):

    params = {
        "engine": "google_scholar",
        "q": search_query,
        "api_key": API_KEY
    }

    # Add year filter
    if year == "Since 2026":
        params["as_ylo"] = "2026"

    elif year == "Since 2025":
        params["as_ylo"] = "2025"

    elif year == "Since 2024":
        params["as_ylo"] = "2024"

    elif year == "Since 2023":
        params["as_ylo"] = "2023"

    elif year == "Since 2022":
        params["as_ylo"] = "2022"

    # Sort option
    if sort_option == "Newest":
        params["as_sdt"] = "1"

    client = serpapi.Client(api_key=API_KEY)

    results = client.search(params)

    return results


# -----------------------------
# SEARCH
# -----------------------------

if search_button:

    if not API_KEY:
        st.error(
            "❌ SerpApi API key not found. "
            "Please add SERPAPI_KEY to your .env file."
        )

    elif not query.strip():
        st.warning(
            "⚠️ Please enter a research topic."
        )

    else:

        with st.spinner("🔎 Searching Google Scholar..."):

            try:

                results = search_scholar(query)

                papers = results.get(
                    "organic_results",
                    []
                )

                if not papers:

                    st.warning(
                        "No research papers found. "
                        "Try another topic."
                    )

                else:

                    st.success(
                        f"✅ Found {len(papers)} research results."
                    )

                    st.divider()

                    # -----------------------------
                    # DISPLAY RESULTS
                    # -----------------------------

                    for index, paper in enumerate(
                        papers,
                        start=1
                    ):

                        title = paper.get(
                            "title",
                            "Untitled Research Paper"
                        )

                        link = paper.get(
                            "link"
                        )

                        snippet = paper.get(
                            "snippet",
                            "No description available."
                        )

                        publication_info = paper.get(
                            "publication_info",
                            {}
                        )

                        summary = publication_info.get(
                            "summary",
                            "Publication information unavailable."
                        )

                        st.markdown(
                            f"## {index}. {title}"
                        )

                        st.write(
                            f"👨‍🔬 **Authors / Publication:** "
                            f"{summary}"
                        )

                        st.write(
                            f"📝 **Description:** {snippet}"
                        )

                        # Citation information
                        inline_links = paper.get(
                            "inline_links",
                            {}
                        )

                        cited_by = inline_links.get(
                            "cited_by",
                            {}
                        )

                        citation_count = cited_by.get(
                            "total",
                            0
                        )

                        st.write(
                            f"📊 **Citations:** "
                            f"{citation_count}"
                        )

                        if link:

                            st.markdown(
                                f"🔗 [Read Research Paper]({link})"
                            )

                        # Resources / PDF
                        resources = paper.get(
                            "resources",
                            []
                        )

                        if resources:

                            for resource in resources:

                                resource_link = resource.get(
                                    "link"
                                )

                                resource_title = resource.get(
                                    "title",
                                    "Available Resource"
                                )

                                if resource_link:

                                    st.markdown(
                                        f"📥 "
                                        f"[{resource_title}]"
                                        f"({resource_link})"
                                    )

                        st.divider()

            except Exception as e:

                st.error(
                    "❌ Something went wrong."
                )

                st.code(
                    str(e)
                )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "Powered by SerpApi Google Scholar API"
)