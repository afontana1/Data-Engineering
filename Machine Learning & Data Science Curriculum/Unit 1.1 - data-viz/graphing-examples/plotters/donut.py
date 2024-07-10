import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d
import mplcursors

import pandas as pd
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d

import ipywidgets as widgets
import seaborn as sns
import ipywidgets as widgets

import pandas as pd

from IPython.display import display
import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import display, clear_output


class SubplotDonutPlotter:
    """Plot Donut Plots showing proportions

    Basic Usage:
        # Assuming df1 and df2 are your DataFrames
        dataframes = [df, df1, df2]

        subplot_donut_plotter = SubplotDonutPlotter()
        # Specify a subset of years (e.g., [2020, 2021]) or leave it as None to include all years
        subset_years = [2020, 2021,2023,2024]
        # Choose aggregation type: 'column' or 'year'
        aggregation_type = 'column'
        subplot_donut_plotter.plot_multi_dataframe_donuts(dataframes, aggregation_type, subset_years)
        subplot_donut_plotter.plot_donut_subplots_by_column(df, subset_years)
        subplot_donut_plotter.plot_donut_subplots_by_year(df, subset_years)
    """

    def plot_donut_subplots_by_column(self, dataframe, subset_years=None):
        if subset_years is not None:
            df_subset = dataframe.loc[subset_years]
        else:
            df_subset = dataframe
        num_plots = len(df_subset.columns)
        cols = int(np.ceil(np.sqrt(num_plots)))
        rows = int(np.ceil(num_plots / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(15, 15))

        for i, column in enumerate(df_subset.columns):
            ax = axes.flatten()[i] if num_plots > 1 else axes
            values = df_subset[column].values
            labels = df_subset.index
            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops=dict(width=0.3),
            )
            ax.axis(
                "equal"
            )  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title(f"Donut Plot - {column}")

        if (num_plots % 2) != 0:
            # Delete the last subplot
            fig.delaxes(axes[rows - 1, cols - 1])

        plt.tight_layout()
        plt.show()

    def plot_donut_subplots_by_year(self, dataframe, subset_years=None):
        if subset_years is not None:
            df_subset = dataframe.loc[subset_years]
        else:
            df_subset = dataframe
        num_plots = len(df_subset.index)
        cols = int(np.ceil(np.sqrt(num_plots)))
        rows = int(np.ceil(num_plots / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(15, 15))

        for i, year in enumerate(df_subset.index.tolist()):
            ax = axes.flatten()[i] if num_plots > 1 else axes
            values = dataframe.T[year].values
            labels = dataframe.T.index

            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops=dict(width=0.3),
            )
            ax.axis(
                "equal"
            )  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title(f"Donut Plot - {year}")

        if (num_plots % 2) != 0:
            # Delete the last subplot
            fig.delaxes(axes[rows - 1, cols - 1])

        plt.tight_layout()
        plt.show()

    def plot_multi_dataframe_donuts(
        self, dataframes, aggregation_type="column", subset_years=None
    ):
        num_plots = len(dataframes)
        cols = int(np.ceil(np.sqrt(num_plots)))
        rows = int(np.ceil(num_plots / cols))

        fig, axes = plt.subplots(
            rows, cols, figsize=(15, 15), gridspec_kw={"hspace": 0.4}
        )

        for i, df in enumerate(dataframes):
            row = i // cols
            col = i % cols
            ax = axes[row, col] if num_plots > 1 else axes
            if aggregation_type == "column":
                self.plot_column_aggregated_donut(ax, df, subset_years)
            elif aggregation_type == "year":
                self.plot_aggregated_donut(ax, df, subset_years)
            ax.set_title(f"Donut Plot - DataFrame {i+1}")

        if (num_plots % 2) != 0:
            # Delete the last subplot
            fig.delaxes(axes[rows - 1, cols - 1])

        # plt.tight_layout()
        plt.show()

    def plot_column_aggregated_donut(self, ax, df, subset_years=None):
        if subset_years is not None:
            df_subset = df.loc[subset_years]
        else:
            df_subset = df

        total_per_column = df_subset.sum(axis=0)
        labels = total_per_column.index

        ax.pie(
            total_per_column.values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.3),
        )
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    def plot_aggregated_donut(self, ax, df, subset_years=None):
        if subset_years is not None:
            df_subset = df.loc[subset_years]
        else:
            df_subset = df

        total_cost_per_year = df_subset.sum(axis=1)
        labels = total_cost_per_year.index

        ax.pie(
            total_cost_per_year.values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.3),
        )
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


class InteractiveDonutPlotter:
    """
    # Example usage:
    # Assuming df1, df2, etc., are your DataFrames
    # Create an instance of the InteractiveDonutPlotter
    interactive_plotter = InteractiveDonutPlotter(dataframes)
    """

    def __init__(self, dataframes):
        self.dataframes = dataframes
        self.subplot_donut_plotter = SubplotDonutPlotter()

        self.subset_years_widget = widgets.SelectMultiple(
            options=list(range(2010, 2050)),
            value=[2010, 2011],
            description="Subset Years:",
        )

        self.aggregation_type_widget = widgets.Dropdown(
            options=["column", "year"], value="column", description="Aggregation Type:"
        )

        self.method_widget = widgets.Dropdown(
            options=[
                "plot_multi_dataframe_donuts",
                "plot_donut_subplots_by_column",
                "plot_donut_subplots_by_year",
            ],
            value="plot_multi_dataframe_donuts",
            description="Method:",
        )

        self.dataframe_widget = widgets.Dropdown(
            options=list(self.dataframes.keys()),
            value=list(self.dataframes.keys())[0],
            description="Select DataFrame:",
        )

        self.plot_button = widgets.Button(description="Plot")
        self.plot_button.on_click(self.plot_donuts)

        self.output_plot = widgets.Output()

        controls = widgets.VBox(
            [
                self.subset_years_widget,
                self.aggregation_type_widget,
                self.method_widget,
                self.dataframe_widget,
                self.plot_button,
            ]
        )

        display(widgets.VBox([controls, self.output_plot]))

    def plot_donuts(self, _):
        with self.output_plot:
            clear_output(wait=True)

            subset_years = self.subset_years_widget.value
            aggregation_type = self.aggregation_type_widget.value
            method = self.method_widget.value
            selected_dataframe_key = self.dataframe_widget.value

            selected_dataframes = {
                key: df for key, df in self.dataframes.items() if df is not None
            }

            if method == "plot_multi_dataframe_donuts":
                self.subplot_donut_plotter.plot_multi_dataframe_donuts(
                    list(selected_dataframes.values()),
                    aggregation_type,
                    list(subset_years),
                )
            elif method == "plot_donut_subplots_by_column":
                selected_df = selected_dataframes[selected_dataframe_key]
                self.subplot_donut_plotter.plot_donut_subplots_by_column(
                    selected_df, list(subset_years)
                )
            elif method == "plot_donut_subplots_by_year":
                selected_df = selected_dataframes[selected_dataframe_key]
                self.subplot_donut_plotter.plot_donut_subplots_by_year(
                    selected_df, list(subset_years)
                )
