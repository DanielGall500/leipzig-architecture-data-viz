import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import os

st.set_page_config(page_title="", layout="wide")

st.title("Sam & Dan's Architecture Map of Leipzig")
st.write("A tour featuring the unusual mixture of Jugenstil and other types of architecture.")

FILE_PATH = "./dataset.csv"

# Function to convert image to base64
def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        return ""

df = pd.read_csv(FILE_PATH)

required_cols = {'latitude', 'longitude', 'title', 'image_path'}
if required_cols.issubset(df.columns):

    def generate_tooltip_html(row):
        img_full_path = os.path.join("images", row["image_path"])
        img_b64 = get_base64_image(img_full_path)
        if img_b64:
            img_html = f"<img src='data:image/jpeg;base64,{img_b64}' width='150'>"
        else:
            img_html = "<i>(image not found)</i>"
        return f"""
            <div style='text-align:left'>
                <b>{row["title"]}</b><br>
                {img_html}
            </div>
        """

    df["tooltip_html"] = df.apply(generate_tooltip_html, axis=1)

    st.subheader("Map Visualisation")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=51.3397,
            longitude=12.3731,
            zoom=11,
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
        ],
        tooltip={"html": "{tooltip_html}", "style": {"backgroundColor": "white", "color": "black"}}
    ))
else:
    st.error("CSV must contain 'latitude', 'longitude', 'title', and 'image_path' columns.")

