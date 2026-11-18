import os
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_interactive_map(df: pd.DataFrame, output_path: str = "seattle_clusters_map.html", sample_size: int = 2000):
    """
    Generates an interactive Folium satellite/street map showing King County Seattle
    housing clusters with color-coded circles and property details in popups.
    """
    if 'lat' not in df.columns or 'long' not in df.columns or 'cluster' not in df.columns:
        raise ValueError("DataFrame must contain 'lat', 'long', and 'cluster' columns.")

    # Center of King County / Seattle
    center_lat = df['lat'].median()
    center_long = df['long'].median()

    m = folium.Map(
        location=[center_lat, center_long],
        zoom_start=10,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri &mdash; King County GIS"
    )

    cluster_colors = {
        -1: "#7f8c8d",  # Outlier: Gray
        0: "#3498db",   # Grade 7: Blue
        1: "#2ecc71",   # Grade 6: Green
        2: "#f39c12",   # Grade 8: Orange
        3: "#9b59b6",   # Grade 11: Purple
        4: "#e74c3c",   # Grade 9: Red
        5: "#1abc9c",   # Grade 10: Teal
    }

    # Sample data to ensure responsive web rendering
    sample_df = df.sample(min(sample_size, len(df)), random_state=42)

    for _, row in sample_df.iterrows():
        cl = int(row['cluster'])
        color = cluster_colors.get(cl, "#34495e")
        popup_text = f"""
        <b>Cluster: {cl}</b><br>
        Price: ${int(row['price']):,}<br>
        Sqft: {int(row['sqft_living']):,} sqft<br>
        Grade: {int(row['grade'])}/13<br>
        Zipcode: {int(row['zipcode']) if pd.notna(row['zipcode']) else 'N/A'}
        """
        folium.CircleMarker(
            location=[row['lat'], row['long']],
            radius=4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=200)
        ).add_to(m)

    m.save(output_path)
    return output_path

def plot_clusters_2d(df: pd.DataFrame, output_image: str = "clusters_price_size.png"):
    """Saves a 2D scatter plot of Price vs. Sqft Living categorized by Cluster."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x='sqft_living',
        y='price',
        hue='cluster',
        palette='Set1',
        alpha=0.6,
        s=25
    )
    plt.title('Phân cụm BĐS Seattle: Giá vs. Diện tích sinh hoạt (DBSCAN)')
    plt.xlabel('Diện tích sinh hoạt (Sqft Living)')
    plt.ylabel('Giá bán (USD)')
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_image, dpi=200)
    plt.close()
    return output_image
