from dash import Output, Input, ctx, State, no_update
import pandas as pd
from dashboard.utilities import filter_data, calculate_kpis, generate_charts
import logging

logger = logging.getLogger(__name__)


def register_callbacks(app_name):
    """
    Registers the callback functions for the Dash app.

    Args:
        app_name: Dash app instance where the callbacks will be registered.
    """

    @app_name.callback(
        [
            Output("chart-1", "figure"),
            Output("chart-2", "figure"),
            Output("chart-3", "figure"),
            Output("chart-4", "figure"),
            Output("table-data", "data"),
            Output("state-data", "data"),
            Output("number-of-videos", "children"),
            Output("avg-number-of-views", "children"),
            Output("avg-number-of-comments", "children"),
            Output("avg-number-of-likes", "children"),
        ],
        [
            Input("chart-1", "clickData"),
            Input("chart-3", "clickData"),
            Input("chart-4", "clickData"),
            Input("master-data", "data"),
            Input("slider-filter", "value"),
            Input("dropdown-filter", "value"),
            Input("state-data", "data"),
            Input("date-picker-range", "start_date"),
            Input("date-picker-range", "end_date"),
        ],
        [
            State("slider-filter", "value"),
            State("dropdown-filter", "value"),
            State("chart-1", "clickData"),
            State("chart-3", "clickData"),
            State("chart-4", "clickData"),
        ],
    )
    def update_dashboard(
        chart1_data,
        chart3_data,
        chart4_data,
        master_data,
        slider_filter,
        dropdown_filter,
        state_data,
        date_start,
        date_end,
        slider_filter_state,
        dropdown_filter_state,
        chart1_state,
        chart3_state,
        chart4_state,
    ):
        """
        Main callback to update all dashboard components.

        Args:
            Inputs: Data and interaction elements from the dashboard.
            States: The previous states of the components.

        Returns:
            Updated figures, table data, filter values, and KPIs.
        """
        # Identify which component triggered the callback
        triggered_id = ctx.triggered_id

        # Step 1: Process master data
        try:
            dff = pd.DataFrame(master_data)
        except ValueError as e:
            logger.error(f"Error converting master_data to DataFrame: {e}")
            return tuple([no_update] * 10)

        try:
            dff, state_data = filter_data(
                dff,
                chart1_state,
                chart3_state,
                chart4_state,
                triggered_id,
                slider_filter_state,
                dropdown_filter_state,
                state_data,
                date_start,
                date_end,
            )
        except Exception as e:
            logger.error(f"Error filtering data: {e}")
            return tuple([no_update] * 10)

        # Step 2: Build charts based on the processed data
        try:
            figg1, figg2, figg3, figg4 = generate_charts(dff)
        except Exception as e:
            logger.error(f"Error building charts: {e}")
            figg1, figg2, figg3, figg4 = no_update, no_update, no_update, no_update

        # Step 3: Calculate key performance indicators (KPIs)
        try:
            (
                number_of_videos,
                avg_number_of_views,
                avg_number_of_comments,
                avg_number_of_likes,
            ) = calculate_kpis(dff)
        except Exception as e:
            logger.error(f"Error calculating KPIs: {e}")
            (
                number_of_videos,
                avg_number_of_views,
                avg_number_of_comments,
                avg_number_of_likes,
            ) = (no_update, no_update, no_update, no_update)
        # Step 4: Prepare data for the table
        table_data = dff.to_dict("records")

        return (
            figg1,
            figg2,
            figg3,
            figg4,
            table_data,
            state_data,
            number_of_videos,
            avg_number_of_views,
            avg_number_of_comments,
            avg_number_of_likes,
        )
