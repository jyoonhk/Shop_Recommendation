import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
import model
doughnut = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "Brands",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2,
            },
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
            },
            "labelLine": {"show": False},
            "data": [
                {"value": 1048, "name": "Uniqlo"},
                {"value": 735, "name": "Adidas"},
                {"value": 580, "name": "Nike"},
                {"value": 484, "name": "Hugo Boss"},
                {"value": 300, "name": "Zara"},
            ],
        }
    ],
}
def app():
    st.write("test page")

    stackedbar = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {
            "data": ["Direct", "Mail Ad", "Affiliate Ad", "Video Ad", "Search Engine"]
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": ["Max_co", "Max Mara", "Ralph Lauren", "Adidas", "Nike", "Hugo Boss", "Uniqlo"],
        },
        "series": [
            {
                "name": "T-Shirts",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [320, 302, 301, 334, 390, 330, 320],
            },
            {
                "name": "Suits",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [120, 132, 101, 134, 90, 230, 210],
            },
            {
                "name": "Shirts",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [220, 182, 191, 234, 290, 330, 310],
            },
            {
                "name": "Shorts",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [150, 212, 201, 154, 190, 330, 410],
            },
            {
                "name": "Dresses",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [820, 832, 901, 934, 1290, 1330, 1320],
            },
        ],
    }
    c1 = st_echarts(options=stackedbar, height="300px")
    c2 = st_echarts(options=doughnut, height="300px")
    c1, c2 = st.beta_columns(2)

