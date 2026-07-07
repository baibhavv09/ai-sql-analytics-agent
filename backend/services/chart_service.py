from typing import Any


class ChartService:
    """
    Service responsible for recommending the most suitable chart
    for SQL query results.

    This service does NOT generate charts.
    It only returns chart metadata for the frontend.
    """

    TIME_KEYWORDS = {
        "date",
        "day",
        "week",
        "month",
        "quarter",
        "year",
        "time",
        "created_at",
        "updated_at",
        "timestamp",
    }

    PERCENTAGE_KEYWORDS = {
        "percentage",
        "percent",
        "share",
        "ratio",
    }

    NUMERIC_TYPES = (int, float)

    def recommend_chart(self, result: dict[str, Any]) -> dict[str, Any]:
        """
        Recommend the best chart for SQL results.

        Parameters
        ----------
        result : dict
            Output from SQLService.execute()

        Returns
        -------
        dict
            Chart metadata
        """

        if not result.get("success"):

            return {
                "chart": "table",
                "reason": "SQL execution failed.",
            }

        columns = result.get("columns", [])
        rows = result.get("rows", [])

        if not rows:

            return {
                "chart": "table",
                "reason": "No data available.",
            }

        if len(columns) < 2:

            return {
                "chart": "table",
                "reason": "At least two columns are required for visualization.",
            }

        x_column = columns[0]
        y_column = columns[1]

        first_value = rows[0][0]
        second_value = rows[0][1]

        x_name = x_column.lower()

        # ---------------------------------------------------
        # Time Series
        # ---------------------------------------------------

        if any(keyword in x_name for keyword in self.TIME_KEYWORDS):

            return {
                "chart": "line",
                "title": f"{y_column} over {x_column}",
                "x_axis": x_column,
                "y_axis": y_column,
                "reason": "Time-series data detected.",
            }

        # ---------------------------------------------------
        # Scatter Plot
        # ---------------------------------------------------

        if isinstance(first_value, self.NUMERIC_TYPES) and isinstance(
            second_value,
            self.NUMERIC_TYPES,
        ):

            return {
                "chart": "scatter",
                "title": f"{y_column} vs {x_column}",
                "x_axis": x_column,
                "y_axis": y_column,
                "reason": "Two numeric columns detected.",
            }

        # ---------------------------------------------------
        # Pie Chart
        # ---------------------------------------------------

        if (
            len(rows) <= 6
            and isinstance(second_value, self.NUMERIC_TYPES)
            and any(
                keyword in y_column.lower()
                for keyword in self.PERCENTAGE_KEYWORDS
            )
        ):

            return {
                "chart": "pie",
                "title": f"{y_column} Distribution",
                "x_axis": x_column,
                "y_axis": y_column,
                "reason": "Small categorical distribution detected.",
            }

        # ---------------------------------------------------
        # Bar Chart
        # ---------------------------------------------------

        if isinstance(second_value, self.NUMERIC_TYPES):

            return {
                "chart": "bar",
                "title": f"{y_column} by {x_column}",
                "x_axis": x_column,
                "y_axis": y_column,
                "reason": "Categorical comparison detected.",
            }

        # ---------------------------------------------------
        # Default
        # ---------------------------------------------------

        return {
            "chart": "table",
            "reason": "No suitable visualization detected.",
        }


chart_service = ChartService()