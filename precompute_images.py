import pandas as pd
import base64
import os

# Paths
CSV_PATH = "./dataset.csv"
IMAGE_FOLDER = "./compressed"
OUTPUT_CSV_PATH = "./precomputed.csv"

def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def generate_tooltip_html(title, image_filename):
    img_path = os.path.join(IMAGE_FOLDER, image_filename)
    img_b64 = get_base64_image(img_path)
    if img_b64:
        img_html = f"<img src='data:image/jpeg;base64,{img_b64}' width='400'>"
    else:
        img_html = "<i>(image not found)</i>"
    return f"""
        <div style='text-align:left'>
            <b>{title}</b><br>
            {img_html}
        </div>
    """

# Load your data
df = pd.read_csv(CSV_PATH)

# Create new column with precomputed HTML
df["tooltip_html"] = df.apply(lambda row: generate_tooltip_html(row["title"], row["image_path"]), axis=1)

# Save to new CSV
df.to_csv(OUTPUT_CSV_PATH, index=False)

print(f"✅ Precomputed tooltips saved to: {OUTPUT_CSV_PATH}")
