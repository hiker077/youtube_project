from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dashboard.utilities import extract_filter_parameters

# Constants
SHADOW_CLASS = "shadow-sm"
CARD_TEXT_CLASS = "card-text fw-bold"
KPI_ICON_COLOR = {"color": "red"}


def create_filter_card(data):
    """
    Create the filter card component.

    Args:
        data: Input data for filters.

    Returns:
        A dbc.Card component containing filters.
    """
    (
        raw_data,
        picker_range_start_date,
        picker_range_end_date,
        range_slider_min,
        range_slider_max,
        dropdown_options,
    ) = extract_filter_parameters(data)

    return dbc.Card(
        dbc.CardBody(
            [
                dcc.Store(id="master-data", data=raw_data),
                dcc.Store(id="state-data"),
                html.H4("Filters", className="mb-4"),
                html.Div(
                    [
                        html.H6("Date", className="mb-3"),
                        dcc.DatePickerRange(
                            id="date-picker-range",
                            month_format="DD/MM/YYYY",
                            end_date_placeholder_text="DD/MM/YYYY",
                            start_date=picker_range_start_date,
                            end_date=picker_range_end_date,
                        ),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [
                        html.H6("Duration of video (minutes)"),
                        dcc.RangeSlider(
                            min=range_slider_min,
                            max=range_slider_max,
                            tooltip={"placement": "bottom", "always_visible": True},
                            allowCross=False,
                            marks=None,
                            id="slider-filter",
                            value=[range_slider_min, range_slider_max],
                        ),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [
                        html.H6("Categories"),
                        dcc.Dropdown(
                            options=dropdown_options,
                            value=dropdown_options,
                            multi=True,
                            id="dropdown-filter",
                        ),
                    ],
                    className="mb-3",
                ),
            ]
        ),
        color="light",
        className="mb-1",
    )


def create_kpi_card(title, icon_class, value_id):
    """
    Create a single KPI card.

    Args:
        title: The title of the KPI.
        icon_class: The Bootstrap icon class for the KPI.
        value_id: The ID of the HTML element displaying the KPI value.

    Returns:
        A dbc.Card component representing the KPI.
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title, className="card-title text-muted"),
                dbc.Row(
                    [
                        dbc.Col(html.I(className=icon_class), style=KPI_ICON_COLOR),
                        dbc.Col(html.H2(id=value_id, className=CARD_TEXT_CLASS)),
                    ],
                    className="align-items-center",
                ),
            ]
        ),
        className=f"{SHADOW_CLASS} my-2",
    )


def create_graph_row():
    """
    Create a row of four graphs.

    Returns:
        A dbc.Row component containing graphs.
    """
    return dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id=f"chart-{i + 1}", config={"displayModeBar": False}),
                className=f"{SHADOW_CLASS} border rounded-3",
            )
            for i in range(4)
        ],
        className="row row-cols-1 row-cols-md-2 row-cols-lg-2 my-4 g-3",
    )


def create_table():
    """
    Create the data table component.

    Returns:
        A dash_table.DataTable wrapped in an HTML div.
    """
    return dash_table.DataTable(
        id="table-data",
        columns=[
            {"name": "Video title", "id": "TITLE", "presentation": "markdown"},
            {"name": "Youtube category", "id": "CATEGORY_TITLE"},
            {"name": "Views", "id": "VIEWCOUNT"},
            {"name": "Likes", "id": "LIKECOUNT"},
            {"name": "Comments", "id": "COMMENTCOUNT"},
            {"name": "Publishing time", "id": "PUBLISHED_PERIOD"},
            {"name": "Week day publishing", "id": "DAY_OF_WEEK_NAME"},
        ],
        page_size=50,
        filter_action="native",
        sort_action="native",
        style_data={"whiteSpace": "normal", "height": "auto"},
        style_header={"fontWeight": "bold"},
        sort_by=[{"column_id": "VIEWCOUNT", "direction": "desc"}],
    )


def create_layout(data, youtube_logo):
    """
    Create the layout for the dashboard.

    Args:
        data: Input data for filters and visualizations.
        youtube_logo: URL or path to the YouTube logo.

    Returns:
        A Dash HTML Div containing the entire layout.
    """
    filter_card = create_filter_card(data)
    kpi_cards = dbc.Row(
        [
            dbc.Col(
                create_kpi_card(
                    "Number of videos", "bi-camera-video", "number-of-videos"
                ),
                width=3,
            ),
            dbc.Col(
                create_kpi_card(
                    "Average number of views", "bi bi-eye-fill", "avg-number-of-views"
                ),
                width=3,
            ),
            dbc.Col(
                create_kpi_card(
                    "Average number of comments",
                    "bi bi-chat-left-text-fill",
                    "avg-number-of-comments",
                ),
                width=3,
            ),
            dbc.Col(
                create_kpi_card(
                    "Average number of likes",
                    "bi bi-hand-thumbs-up-fill",
                    "avg-number-of-likes",
                ),
                width=3,
            ),
        ],
        className="my-4",
    )
    graph_row = create_graph_row()
    table = create_table()

    return html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    html.Img(src=youtube_logo, height="40px"),
                                    className="my-3",
                                ),
                                html.Div(
                                    "Analyse your favourite channel statistics",
                                    className="fst-italic fs-4 my-4",
                                ),
                                filter_card,
                            ],
                            md=2,
                        ),
                        dbc.Col(
                            [
                                kpi_cards,
                                graph_row,
                                dbc.Row(
                                    dbc.Col(
                                        table, className="justify-content-center my-2"
                                    )
                                ),
                            ],
                            md=10,
                        ),
                    ],
                    className="mx-3",
                ),
            ],
            fluid=True,
            className="bg-light",
        )
    )
