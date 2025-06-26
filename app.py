import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import os

st.set_page_config(page_title="", layout="wide")

st.title("Sam & Dan's Quirky Architecture of (West) Leipzig")

FILE_PATH = "./dataset.csv"

# Function to convert image to base64
@st.cache_data
def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        return ""

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

@st.cache_data
def prepare_data(df):
    def generate_tooltip_html(row):
        img_full_path = os.path.join("compressed", row["image_path"])
        try:
            with open(img_full_path, "rb") as f:
                data = f.read()
                img_b64 = base64.b64encode(data).decode()
                img_html = f"<img src='data:image/jpeg;base64,{img_b64}' width='150'>"
        except Exception as e:
            img_html = "<i>(image not found)</i>"

        return f"""
            <div style='text-align:left'>
                <b>{row["title"]}</b><br>
                {img_html}
            </div>
        """
    df["tooltip_html"] = df.apply(generate_tooltip_html, axis=1)
    return df

df = pd.read_csv("precomputed.csv")
required_cols = {'latitude', 'longitude', 'title', 'image_path'}
if required_cols.issubset(df.columns):

    # df = prepare_data(df)

    st.subheader("Map")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=51.333839,
            longitude=12.329561,
            zoom=13,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[longitude, latitude]',
                get_radius=25,
                get_color='[255, 100, 100, 160]',
                pickable=True,
            ),
            pdk.Layer(
                "TextLayer",
                data=df,
                get_position='[longitude, latitude]',
                get_text="title",
                get_size=12,
                get_color=[255, 255, 255],
                get_angle=0,
                get_alignment_baseline="'bottom'",
            )
        ],
        tooltip={"html": "{tooltip_html}", "style": {"backgroundColor": "white", "color": "black"}}
    ))
else:
    st.error("CSV must contain 'latitude', 'longitude', 'title', and 'image_path' columns.")

