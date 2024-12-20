import streamlit as st
from streamlit_elements import elements, dashboard, mui, nivo

# Set Streamlit page configuration to wide
st.set_page_config(page_title="Anime Viewer Analysis", layout="wide")
# Dashboard
st.title("Anime Viewer Analysis Dashboard")

DATA = [
    {"taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114},
    {"taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72},
    {"taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99},
    {"taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30},
    {"taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103},
]



with elements("dashboard"):

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print("changed")
        print(updated_layout)

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 6, 4, minW=3, minH=3),
        dashboard.Item("second_item", 6, 0, 6, 4, minH=3),
        dashboard.Item("third_item", 0, 1, 12, 5, minW=3, minH=4),
        dashboard.Item("forth_item", 0, 2, 5, 3, minW=2, minH=4),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.
    with dashboard.Grid(layout, rowHeight=57, margin=[30, 30], onLayoutChange=handle_layout_change):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item", key="second_item")
        mui.Paper("Third item (cannot drag)", key="third_item")

        with mui.Paper(key="forth_item",
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Radar(
                    data=DATA,
                    keys=[ "chardonay", "carmenere", "syrah" ],
                    indexBy="taste",
                    valueFormat=">-.2f",
                    margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                    borderColor={ "from": "color" },
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor={ "theme": "background" },
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ],
                    theme={
                        "background": "#FFFFFF",
                        "textColor": "#31333F",
                        "tooltip": {
                            "container": {
                                "background": "#FFFFFF",
                                "color": "#31333F",
                            }
                        }
                    }
                )