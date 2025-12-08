import streamlit as st
from st_tabs import TabBar
import pandas as pd
import json

st.set_page_config(page_title="William Alex Wong | Portfolio", layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap');
    .block-container {
        padding-top: 1rem;
    }
    html, body, [class*="css"] {
        font-family: 'EB Garamond', sans-serif;
    }
    .stButton button:hover {
        border: 1px solid #060680ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# links
my_linkedin = "http://www.linkedin.com/in/william-alex-wong/"
my_ticker = "https://theticker.org/staff_name/william-alex-wong/"

links = [
    my_linkedin,
    my_ticker
]

img_linkedin = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/1024px-LinkedIn_icon.svg.png"
img_ticker = "https://yt3.googleusercontent.com/_2N61zOdExgaaZb4D7BlAEuqThe7WcWVGb0Yqfc2jUF3uSXVyONlCeEvrj4bVWB7DyMn-A4cOA=s900-c-k-c0x00ffffff-no-rj"

icon_images = [
    img_linkedin,
    img_ticker
]



## -- top summary
col1, col2 = st.columns([3, 4])

with col1:
    st.title("William Alex Wong")

    html = "<div style='display: flex; gap: 10px;'>"
    for link, img in zip(links, icon_images):
        html += f'<a href="{link}" target="_blank"><img src="{img}" width="24" style="display: block;"></a>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


with col2:
    st.write("")

st.markdown("")



## -- tabs
tab = TabBar(
    tabs=["Publications", "Resume"],
    default=0,
    fontSize="18px",
    fontWeight="600",
    color="#11111aff",
    activeColor="#010154",
)



if tab == 0:
    # st.subheader("Publications")
    df = pd.read_csv("data/publications.csv", sep=";")
    # sort starred pubs first
    df_sorted = df.sort_values(by='star', ascending=False).reset_index(drop=True)
    df_sorted.loc[df_sorted['star'] == 'Y', 'title'] = '⭐ ' + df_sorted.loc[df_sorted['star'] == 'Y', 'title'].astype(str)

    # filter: year
    df_sorted['year'] = pd.to_datetime(df_sorted['timeframe'], errors='coerce').dt.year.astype('Int64')
    years = [str(int(y)) for y in sorted(df_sorted['year'].dropna().unique())]
    # filter: pub
    pubs = sorted(df_sorted['pub'].dropna().unique())

    if 'selected_years' not in st.session_state:
        st.session_state.selected_years = years
    if 'selected_pubs' not in st.session_state:
        st.session_state.selected_pubs = pubs

    # reset filters
    def reset_filters():
        st.session_state.selected_years = years
        st.session_state.selected_pubs = pubs


    # page filters, reset
    _, col1, col2, col3, _ = st.columns([0.25, 3, 3, 1, 0.25])
    with col1:
        selected_years = st.multiselect("Filter by Year", options=years, key='selected_years')
    with col2:
        selected_pubs = st.multiselect("Filter by Publication", options=pubs, key='selected_pubs')
    with col3:
        st.write("")
        st.write("")
        st.button("Reset Filters", on_click=reset_filters, width='stretch')

    filtered_df = df_sorted[
        ((len(st.session_state.selected_years) == 0) | (df_sorted['year'].astype(str).isin(st.session_state.selected_years))) 
        &
        ((len(st.session_state.selected_pubs) == 0) | (df_sorted['pub'].isin(st.session_state.selected_pubs)))
    ].reset_index(drop=True)


    # pub articles here
    st.write("")
    col1, spc, col2, spc, col3 = st.columns([3, 0.1, 3, 0.1, 3], gap="small")
    columns = [col1, col2, col3]

    for idx, row in filtered_df.iterrows():
        col_idx = idx % 3
        with columns[col_idx]:
            url = row['url'] if pd.notna(row['url']) else ""
            # clickable container to url
            html = f'''
                <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
                <div style="border: 1px solid #ddd; padding: 10px; padding-left: 12.5px; margin-bottom: 20px; border-radius: 8px; cursor: pointer;">
                    <h4>{row['title']}</h4>
                    <div style="
                        display: flex; 
                        justify-content: center; 
                        align-items: center; 
                        font-size: 0.9rem; 
                        color: #060680ff;
                        gap: 8px;
                    ">
                        <span>{row['timeframe']}</span>
                        <span style="user-select:none;">|</span>
                        <span style="text-transform: uppercase;">{row['pub'] if 'pub' in row else ''}</span>
                    </div>
                    <div style="margin-top: 10px;">
            '''
            image_url = row['image'] if pd.notna(row['image']) else ""
            if image_url:
                html += f'<img src="{image_url.strip()}" alt="Image" style="width: 100%; border-radius: 6px; margin-bottom: 10px;">'
            html += '''
                </div>
            </div>
            </a>
            '''
            st.markdown(html, unsafe_allow_html=True)
            st.divider()




if tab == 1:
    st.markdown("##### Education")
    education = {
        'College / University': ['CUNY Baruch College'],
        'Major / Degree': ["History, B.A."],
        'Minor / Concentration': ['Asian and Asian American Studies'],
        'GPA': ['3.93'],
        'Honors & Awards': ['Dean’s List 2024, Dean’s List 2025'],
        'Graduation Date': ['Expected December 2025'],
    }
    df_education = pd.DataFrame(education)
    st.dataframe(df_education, hide_index=True)

    # st.markdown("---")

    # st.subheader("Resume")
    with open("resume.pdf", "rb") as f:
        pdf_bytes = f.read()
        st.pdf(pdf_bytes)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.markdown(">Last updated: October 2025")
    with col2:
        btn = st.download_button(
            label="Download Resume (PDF)",
            data=pdf_bytes,
            file_name="resume.pdf",
            mime="application/pdf",
            width='stretch'
        )
    with col3:
        st.write("")
