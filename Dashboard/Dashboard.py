"""Dashboard réseau + géospatial avec cuxfilter (RAPIDS, GPU requis).

Exemple complet (préparation de `final_df` et `edges`) :
https://github.com/rapidsai-community/showcase/tree/main/team_contributions/cuxfilter-tutorial
"""
import cuxfilter


def build_dashboard(final_df, edges):
    """Construit le dashboard à partir des nœuds (`final_df`) et arêtes (`edges`) cuDF."""
    cux_df = cuxfilter.DataFrame.load_graph((final_df, edges))

    # Charts
    chart1 = cuxfilter.charts.graph(
        edge_source="src",
        edge_target="dst",
        edge_color_palette=["gray", "black"],
        node_pixel_shade_type="linear",
        edge_render_type="curved",  # curved, direct
        edge_transparency=0.6,  # 0.1 – 0.9
        title="ForceAtlas2 Graph",
    )
    chart2 = cuxfilter.charts.scatter(
        x="x_original",
        y="y_original",
        tile_provider="CARTODBPOSITRON",
        point_size=4,
        pixel_shade_type="linear",
        pixel_spread="spread",
        title="Scatter Layout",
    )
    chart3 = cuxfilter.charts.bar("hour", title="Trips per hour")
    chart4 = cuxfilter.charts.bar("from_station_id", title="Source station")
    chart5 = cuxfilter.charts.bar("to_station_id", title="Destination station")

    # Widgets
    widget1 = cuxfilter.charts.multi_select("year")
    widget2 = cuxfilter.charts.multi_select(
        "day_type", label_map={0: "weekday", 1: "weekend", "": "all"}
    )

    return cux_df.dashboard(
        [chart1, chart2, chart3, chart4, chart5],
        sidebar=[widget1, widget2],
        layout_array=[[1, 1, 2], [1, 1, 2], [3, 4, 5]],
        theme=cuxfilter.themes.rapids,
        title="Network and Geospatial Graph",
    )


if __name__ == "__main__":
    raise SystemExit(
        "Importe build_dashboard(final_df, edges) après avoir préparé les données "
        "(voir le tutoriel cité en tête de fichier), puis appelle .show()."
    )
