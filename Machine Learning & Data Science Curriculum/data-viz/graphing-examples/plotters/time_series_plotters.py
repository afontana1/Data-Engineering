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

from functools import partial
from IPython.display import display, clear_output

import pandas as pd


# If widgets are not rendering or interactivity is not working
# https://github.com/jupyterlab/jupyterlab/issues/12580

# using plotly
# https://saturncloud.io/blog/troubleshooting-plotly-chart-not-showing-in-jupyter-notebook/


class TimeSeriesPlotter:
    def __init__(self, dataframe, kind="Columns"):
        self.dataframe = dataframe
        self.kind = "Columns"

    def plot_interactive_time_series(
        self,
        columns_subset=None,
        years_subset=None,
        scale_factor=None,
        growth_rate=None,
        show_original=False,
        moving_average_window=None,
        plot_original_moving_average=False,
        plot_scaled_on_original=False,
        plot_growth_rate_moving_average=False,
        plot_growth_rate_on_original=False,
    ):
        """
        Plot interactive time series with optional scaling, growth rate, and moving average.

        Parameters:
            columns_subset (list, optional): List of columns to be plotted. Default is all columns in the dataframe.
            years_subset (list, optional): List of years to be plotted. Default is all years in the dataframe.
            scale_factor (float, optional): Factor to scale the values by. Default is None.
            growth_rate (float, optional): Compound growth rate to apply to the values. The formula used is:
                new_value = original_value * (1 + growth_rate)^t, where t is the number of periods.
                Default is None.
            show_original (bool, optional): Whether to show the original values. Default is True.
            moving_average_window (int, optional): Window size for calculating the moving average. Default is None.
            plot_original_moving_average (bool, optional): Whether to plot moving average and error bars for the original series. Default is False.
            plot_scaled_moving_average (bool, optional): Whether to plot moving average and error bars for the scaled series. Default is False.
            plot_scaled_on_original (bool, optional): Whether to plot the scaled series on the original plot. Default is False.

        Returns:
            None

        Basic Usage:

            ts_plotter = TimeSeriesPlotter(df)

            ts_plotter.plot_interactive_time_series(
                columns_subset=['Column1', 'Column2'],
                years_subset = None,
                scale_factor=None,
                show_original = True,
                growth_rate = 0.02,
                moving_average_window=3,
                plot_original_moving_average=False,
                plot_scaled_on_original = False,
                plot_growth_rate_moving_average=True,
                plot_growth_rate_on_original=True
            )

        """
        if columns_subset is None:
            columns_subset = self.dataframe.columns

        if years_subset is None:
            years_subset = self.dataframe.index

        num_columns = len(columns_subset)
        num_rows = 1 if num_columns == 1 else num_columns
        # Create subplots
        fig, axs = plt.subplots(
            nrows=num_rows,
            ncols=2,
            figsize=(16, 5 * num_rows),
        )
        # If there's only one column to plot, adjust axes accordingly
        if num_columns == 1:
            axs = axs.reshape(1, -1)

        for i, column in enumerate(columns_subset):
            values = self.dataframe.loc[years_subset, column].values

            # Plot time series on the left plot
            if show_original:
                axs[i, 0].plot(
                    years_subset, values, label=f"Original {column}", linestyle="-"
                )

                # Plot moving average with error bars if specified
                if moving_average_window is not None and plot_original_moving_average:
                    moving_avg = (
                        pd.Series(values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .mean()
                    )
                    axs[i, 0].plot(
                        years_subset,
                        moving_avg,
                        label=f"Original Moving Avg {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                    # Calculate standard deviation for error bars
                    std_dev = (
                        pd.Series(values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .std()
                    )
                    upper_bound = moving_avg + std_dev
                    lower_bound = moving_avg - std_dev
                    axs[i, 0].fill_between(
                        years_subset,
                        lower_bound,
                        upper_bound,
                        alpha=0.2,
                        label="Original Error Bars",
                    )

                axs[i, 0].set_ylabel("Values")
                axs[i, 0].legend()

            # Apply scaling factor if specified
            if (scale_factor is not None) and (scale_factor != 0.0):
                scaled_values = values * scale_factor

                if plot_scaled_on_original:
                    axs[i, 0].plot(
                        years_subset,
                        scaled_values,
                        label=f"Scaled {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                axs[i, 0].set_ylabel("Values")
                axs[i, 0].legend()

            # Calculate and plot series with new compound growth rate on the left plot
            if (growth_rate is not None) and (growth_rate != 0.0):
                # Calculate the series under the new compound growth rate
                periods = np.arange(1, len(years_subset) + 1)
                growth_values = values * (1 + growth_rate) ** periods
                # growth_values = values * np.power(1 + growth_rate, periods)

                if plot_growth_rate_on_original:
                    axs[i, 0].plot(
                        years_subset,
                        growth_values,
                        label=f"With Growth Rate {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                # Plot delta on the right plot
                delta = growth_values - values
                axs[i, 1].bar(
                    years_subset,
                    delta,
                    label=f"Delta (Growth Rate {column})",
                    alpha=0.7,
                )

                axs[i, 1].set_ylabel("Delta")
                axs[i, 1].legend()

                # Plot scaled moving average with error bars if specified
                if (
                    plot_growth_rate_moving_average
                    and moving_average_window is not None
                ):
                    growth_moving_avg = (
                        pd.Series(growth_values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .mean()
                    )
                    axs[i, 0].plot(
                        years_subset,
                        growth_moving_avg,
                        label=f"Growth Moving Avg {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                    # Calculate standard deviation for error bars
                    scaled_std_dev = (
                        pd.Series(growth_values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .std()
                    )
                    scaled_upper_bound = growth_moving_avg + scaled_std_dev
                    scaled_lower_bound = growth_moving_avg - scaled_std_dev
                    axs[i, 0].fill_between(
                        years_subset,
                        scaled_lower_bound,
                        scaled_upper_bound,
                        alpha=0.2,
                        label="Growth Error Bars",
                    )

            handles, labels = axs[i, 0].get_legend_handles_labels()
            axs[i, 0].legend(handles, labels, loc="best")

        axs[-1, 0].set_xlabel("Year")
        axs[-1, 1].set_xlabel("Year")

        plt.suptitle(f"{self.kind}")

        # Adjust layout to ensure the legend is visible
        plt.tight_layout()

        plt.show()

    def apply_growth_rate(self, series, growth_rate):
        """
        Apply compound growth rate to a time series.

        Parameters:
        - series (pd.Series): Time series data to apply the growth rate to.
        - growth_rate (float): Compound growth rate.

        Returns:
        - pd.Series: Time series with applied growth rate.
        """
        periods = len(series)
        index = series.index
        adjusted_series = pd.Series(index=index, dtype=float)

        for t in range(periods):
            adjusted_series[index[t]] = series[index[t]] * (1 + growth_rate) ** t

        return adjusted_series

    def plot_multiple_time_series(
        self,
        columns_subset=None,
        years_subset=None,
        growth_rates=None,
        show_original=True,
    ):
        """
        Plot multiple time series on one plot with optional compound growth rates.

        Parameters:
        - columns_subset (list or None): List of column names to be plotted. If None, plot all columns.
        - years_subset (list or None): List of years to be plotted. If None, plot all years.
        - growth_rates (dict or None): Dictionary where keys are column names, and values are growth rates.

        Example:
            ts_plotter = TimeSeriesPlotter(df)
            columns_to_plot = ['Column1', 'Column2']
            years_to_plot = [2010, 2015, 2020]
            growth_rates_dict = {'Column1': 0.05, 'Column2': -0.02}

            ts_plotter.plot_multiple_time_series(
                columns_subset=['Column1', 'Column2'],
                years_subset = None,
                growth_rates = growth_rates_dict
            )
        """
        # If columns_subset is None, plot all columns
        if columns_subset is None:
            columns_subset = self.dataframe.columns.tolist()

        # If years_subset is None, plot all years
        if years_subset is None:
            years_subset = self.dataframe.index.tolist()

        # Check if the provided columns_subset and years_subset are valid
        for column in columns_subset:
            if column not in self.dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the dataframe.")
        for year in years_subset:
            if year not in self.dataframe.index:
                raise ValueError(f"Year '{year}' not found in the dataframe index.")

        # Subset the dataframe based on the provided columns_subset and years_subset
        subset_df = self.dataframe.loc[years_subset, columns_subset]

        # Plot the original time series
        plt.figure(figsize=(10, 6))
        for column in columns_subset:

            if show_original:
                plt.plot(
                    subset_df.index, subset_df[column], label=f"{column} (Original)"
                )

            # Apply growth rate if provided
            if growth_rates and (column in growth_rates):
                adjusted_series = self.apply_growth_rate(
                    subset_df[column], growth_rates[column]
                )
                plt.plot(
                    subset_df.index,
                    adjusted_series,
                    linestyle="--",
                    label=f"{column} (Adjusted)",
                )

        # Set plot labels and title
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.title("Multiple Time Series Plot with Growth Rates")

        # Show legend
        plt.legend()

        # Display the plot
        plt.show()

    def plot_time_series_with_distribution(
        self, column_subset=None, year_subset=None, growth_rate=None
    ):
        """
        Plot time series and their distributions on a plot.

        Parameters:
        - column_subset (list or None): List of column names to be plotted. If None, plot all columns.
        - year_subset (list or None): List of years to be plotted. If None, plot all years.
        - growth_rate (float, optional): Compound growth rate to apply to the values.

        Basic Usage:
            columns_to_plot = ['Column1', 'Column2', 'Column3']
            years_to_plot = None
            growth_rate_to_apply = 0.05

            ts_plotter.plot_time_series_with_distribution(columns_to_plot, years_to_plot, growth_rate_to_apply)
        """
        # If column_subset is None, plot all columns
        if column_subset is None:
            column_subset = self.dataframe.columns.tolist()

        # If year_subset is None, plot all years
        if year_subset is None:
            year_subset = self.dataframe.index.tolist()

        # Check if the provided column_subset and year_subset are valid
        for column in column_subset:
            if column not in self.dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the dataframe.")
        for year in year_subset:
            if year not in self.dataframe.index:
                raise ValueError(f"Year '{year}' not found in the dataframe index.")

        num_columns = len(column_subset)
        num_rows = 1 if num_columns == 1 else num_columns
        # Create subplots
        fig, axes = plt.subplots(
            nrows=num_rows,
            ncols=3,
            figsize=(18, 5 * num_rows),
            gridspec_kw={"width_ratios": [3, 1, 1]},
        )
        # If there's only one column to plot, adjust axes accordingly
        if num_columns == 1:
            axes = axes.reshape(1, -1)

        # Iterate over specified columns
        for i, column_name in enumerate(column_subset):
            # Get the specified time series
            original_series = self.dataframe.loc[year_subset, column_name]
            # Apply growth rate if provided
            if growth_rate is not None:
                adjusted_series = self.apply_growth_rate(original_series, growth_rate)

                # Plot the original time series
                axes[i, 0].plot(
                    original_series.index, original_series, label="Original"
                )
                axes[i, 0].plot(
                    original_series.index, adjusted_series, label="Adjusted"
                )
                axes[i, 0].set_title(f"Time Series Plot - {column_name}")
                axes[i, 0].set_xlabel("Year")
                axes[i, 0].set_ylabel("Value")
                axes[i, 0].legend()

                # Plot the distribution of the original series
                sns.histplot(original_series, kde=True, ax=axes[i, 1])
                axes[i, 1].set_title(f"Original Distribution - {column_name}")
                axes[i, 1].set_xlabel("Value")
                axes[i, 1].set_ylabel("Density")

                # Plot the distribution of the adjusted series
                sns.histplot(adjusted_series, kde=True, ax=axes[i, 2])
                axes[i, 2].set_title(f"Adjusted Distribution - {column_name}")
                axes[i, 2].set_xlabel("Value")
                axes[i, 2].set_ylabel("Density")

                # Set x-axis range for distribution plots
                x_min = min(original_series.min(), adjusted_series.min())
                x_max = max(original_series.max(), adjusted_series.max())
                axes[i, 1].set_xlim(x_min, x_max)
                axes[i, 2].set_xlim(x_min, x_max)

            else:
                # If no growth rate provided, plot only the original time series and its distribution
                # Plot the original time series
                axes[i, 0].plot(
                    original_series.index, original_series, label="Original"
                )
                axes[i, 0].set_title(f"Time Series Plot - {column_name}")
                axes[i, 0].set_xlabel("Year")
                axes[i, 0].set_ylabel("Value")
                axes[i, 0].legend()

                # Plot the distribution of the original series
                sns.histplot(original_series, kde=True, ax=axes[i, 1])
                axes[i, 1].set_title(f"Original Distribution - {column_name}")
                axes[i, 1].set_xlabel("Value")
                axes[i, 1].set_ylabel("Density")

        # Adjust layout
        plt.tight_layout()

        # Display the plot
        plt.show()

    def plot_area_under_curve(
        self, column_subset=None, year_subset=None, growth_rate=None
    ):
        """
        Plot the area under the curve for specified time series.

        Parameters:
        - column_subset (list or None): List of column names to be plotted. If None, plot all columns.
        - year_subset (list or None): List of years to be considered. If None, consider all years.
        - growth_rate (float, optional): Compound growth rate to apply to the values.

        Basic Usage:
            columns_to_plot = ['Column1', 'Column2']
            years_to_plot = None
            growth_rate_to_apply = 0.05

            ts_plotter.plot_area_under_curve(column_subset = columns_to_plot, year_subset = years_to_plot,  growth_rate=growth_rate_to_apply)
        """
        # If column_subset is None, plot all columns
        if column_subset is None:
            column_subset = self.dataframe.columns.tolist()

        # If year_subset is None, consider all years
        if year_subset is None:
            year_subset = self.dataframe.index.tolist()

        # Create subplots
        num_plots = len(column_subset)
        fig, axes = plt.subplots(
            nrows=num_plots, ncols=1, figsize=(10, 6 * num_plots), sharex=True
        )

        # Iterate over specified columns
        for i, column_name in enumerate(column_subset):
            # Get the specified time series
            original_series = self.dataframe.loc[year_subset, column_name]

            # Apply growth rate if provided
            if growth_rate is not None:
                adjusted_series = self.apply_growth_rate(original_series, growth_rate)

                # Plot the original and adjusted time series
                # axes[i].plot(original_series.index, original_series, label="Original")
                axes[i].plot(original_series.index, adjusted_series, label="Adjusted")
                # axes[i].fill_between(original_series.index, original_series, adjusted_series, color='gray', alpha=0.5, label='Area Under Curve')
                axes[i].set_ylabel("Value")
                axes[i].set_title(
                    f"Time Series Plot with Area Under Curve - {column_name}"
                )
                axes[i].legend()

            # If no growth rate provided, plot only the original time series
            axes[i].plot(original_series.index, original_series, label="Original")
            axes[i].fill_between(
                original_series.index,
                0,
                original_series,
                color="gray",
                alpha=0.5,
                label="Area Under Curve",
            )
            axes[i].set_ylabel("Value")
            axes[i].set_title(f"Time Series Plot with Area Under Curve - {column_name}")
            axes[i].legend()

        # Set x-axis label and adjust layout
        plt.xlabel("Year")
        plt.tight_layout()

        # Display the plot
        plt.show()

    def plot_heatmap(self, column_subset=None, year_subset=None, growth_rate=None):
        """
        Create two heatmaps of multiple time series: one for original values and one after growth rate has been applied.

        Parameters:
        - column_subset (list or None): List of column names to be included in the heatmap. If None, include all columns.
        - year_subset (list or None): List of years to be included in the heatmap. If None, include all years.
        - growth_rate (float, optional): Compound growth rate to apply to the values.

        Basic Usage:
            # Specify the columns, years, and growth rate for plotting
            columns_to_plot = None
            years_to_plot = None
            growth_rate_to_apply = 0.05

            # Plot the two heatmaps for the specified time series
            ts_plotter.plot_heatmap(columns_to_plot, years_to_plot, growth_rate_to_apply)
        """
        # If column_subset is None, include all columns
        if column_subset is None:
            column_subset = self.dataframe.columns.tolist()

        # If year_subset is None, include all years
        if year_subset is None:
            year_subset = self.dataframe.index.tolist()

        # Check if the provided column_subset and year_subset are valid
        for column in column_subset:
            if column not in self.dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the dataframe.")
        for year in year_subset:
            if year not in self.dataframe.index:
                raise ValueError(f"Year '{year}' not found in the dataframe index.")

        # Create a subset of the dataframe based on column_subset and year_subset
        subset_df = self.dataframe.loc[year_subset, column_subset]

        # Apply growth rate if provided
        if growth_rate is not None:
            adjusted_df = subset_df.apply(
                lambda series: self.apply_growth_rate(series, growth_rate)
            )

            # Plot two heatmaps side by side
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

            # Heatmap for original values
            sns.heatmap(
                subset_df.T,
                cmap="YlGnBu",
                annot=False,
                fmt=".2f",
                cbar_kws={"label": "Value"},
                ax=axes[0],
            )
            axes[0].set_title("Heatmap of Original Values")
            axes[0].set_xlabel("Year")
            axes[0].set_ylabel("Time Series")

            # Heatmap for values after growth rate has been applied
            sns.heatmap(
                adjusted_df.T,
                cmap="YlGnBu",
                annot=False,
                fmt=".2f",
                cbar_kws={"label": "Value"},
                ax=axes[1],
            )
            axes[1].set_title("Heatmap after Growth Rate Application")
            axes[1].set_xlabel("Year")
            axes[1].set_ylabel("Time Series")

            # Adjust layout
            plt.tight_layout()

            # Display the plot
            plt.show()

        else:
            # If no growth rate provided, plot only the heatmap for original values
            plt.figure(figsize=(12, 8))
            sns.heatmap(
                subset_df.T,
                cmap="YlGnBu",
                annot=False,
                fmt=".2f",
                cbar_kws={"label": "Value"},
            )
            plt.title("Heatmap of Original Values")
            plt.xlabel("Year")
            plt.ylabel("Time Series")
            plt.show()


class TimeSeriesVisualizer:
    """This simply visualizes the data using other methods

    Basic Usage:

        plotter = TimeSeriesVisualizer(df)

        plotter.plot_horizontal_bar_chart(columns=['Column1', 'Column2'], years=None)
        plotter.plot_horizontal_bar_subplots(columns=['Column1', 'Column2'], years=None, growth_rate=0.05)
        plotter.plot_overlapping_bar(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_overlapping_stacked_bar(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_overlapping_area_lines(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_stacked_area_chart(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_stacked_ratio_chart(columns=['Column1', 'Column2', 'Column3'], years=None)
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def calculate_growth_values(self, values, growth_rate):
        t = np.arange(len(values))
        growth_values = values * (1 + growth_rate) ** t
        return growth_values

    def plot_horizontal_bar_chart(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        data_to_plot.plot(kind="barh", stacked=True)
        plt.xlabel("Values")
        plt.ylabel("Time")
        plt.title("Horizontal Bar Chart")
        plt.show()

    def plot_horizontal_bar_subplots(self, columns=None, years=None, growth_rate=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        num_columns = len(columns)
        num_rows = 1 if num_columns == 1 else num_columns
        fig, axes = plt.subplots(
            nrows=num_rows, ncols=1, figsize=(10, 5 * num_rows), squeeze=False
        )

        for i, col in enumerate(columns):
            data_to_plot = self.dataframe.loc[years, col]

            if growth_rate is not None:
                growth_values = self.calculate_growth_values(
                    data_to_plot.values, growth_rate
                )
                axes[i, 0].barh(
                    data_to_plot.index,
                    data_to_plot,
                    color="black",
                    label="Original Series",
                )
                axes[i, 0].barh(
                    data_to_plot.index,
                    growth_values,
                    color="green",
                    alpha=0.7,
                    label=f"Growth Rate: {growth_rate}",
                )
            else:
                axes[i, 0].barh(
                    data_to_plot.index,
                    data_to_plot,
                    color="blue",
                    label="Original Series",
                )

            axes[i, 0].set_xlabel("Values")
            axes[i, 0].set_ylabel("Time")
            axes[i, 0].set_title(f"Horizontal Bar Chart - {col}")
            axes[i, 0].legend()

        plt.tight_layout()
        plt.show()

    def plot_overlapping_bar(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        num_series = len(columns)
        colors = plt.cm.Set1(
            range(num_series)
        )  # Using Set1 color map for distinct colors

        data_to_plot = self.dataframe.loc[years, columns]
        ax = data_to_plot.plot(
            kind="bar", alpha=0.4, color=colors, edgecolor="black", width=0.8
        )  # Set width for complete overlap
        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("Overlapping Bar Chart")
        ax.legend(columns)

        plt.show()

    def plot_overlapping_stacked_bar(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        data_to_plot_percentage = data_to_plot.div(
            data_to_plot.sum(axis=1), axis=0
        )  # Normalize by row to get proportions

        num_series = len(columns)
        colors = plt.cm.Set1(
            range(num_series)
        )  # Using Set1 color map for distinct colors

        ax = data_to_plot_percentage.plot(
            kind="bar",
            stacked=True,
            alpha=0.7,
            color=colors,
            edgecolor="black",
            width=0.8,
        )
        ax.set_xlabel("Time")
        ax.set_ylabel("Proportion of Total")
        ax.set_title("Overlapping Stacked Bar Chart")
        ax.legend(columns)

        plt.show()

    def plot_overlapping_area_lines(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        colors = plt.cm.Set1(range(len(columns)))
        fig, ax = plt.subplots(1, 1, figsize=(18, 6))

        for i, col in enumerate(columns):
            y_values = data_to_plot[col].values
            ax.plot(data_to_plot.index, y_values, color=colors[i], label=col)
            ax.fill_between(data_to_plot.index, 0, y_values, color=colors[i], alpha=0.4)

        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("Overlapping Area Line Chart")
        ax.legend()

        plt.show()

    def plot_stacked_area_chart(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        colors = plt.cm.Set1(range(len(columns)))
        fig, ax = plt.subplots(1, 1, figsize=(18, 6))

        stacked_data = data_to_plot.cumsum(axis=1)

        for i, col in enumerate(columns):
            if i == 0:
                ax.fill_between(
                    data_to_plot.index,
                    0,
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )
            else:
                ax.fill_between(
                    data_to_plot.index,
                    stacked_data[columns[i - 1]],
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )

        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("Stacked Area Chart")
        ax.legend()

        plt.show()

    def plot_stacked_ratio_chart(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        colors = plt.cm.Set1(range(len(columns)))
        fig, ax = plt.subplots(1, 1, figsize=(18, 6))

        total = data_to_plot.sum(axis=1)
        stacked_data = data_to_plot.div(total, axis=0).cumsum(axis=1)

        for i, col in enumerate(columns):
            if i == 0:
                ax.fill_between(
                    data_to_plot.index,
                    0,
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )
            else:
                ax.fill_between(
                    data_to_plot.index,
                    stacked_data[columns[i - 1]],
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )

        ax.set_xlabel("Time")
        ax.set_ylabel("Ratio")
        ax.set_title("Multiple Stacked Ratio Chart")
        ax.legend()

        plt.show()


class InteractiveTimeSeriesPlot:
    def __init__(self, df, scale_factor_df):
        self.df = df
        self.scale_factor_df = scale_factor_df
        self.output = widgets.Output()

        self.columns_subset_widget = widgets.SelectMultiple(
            options=df.columns.tolist(),
            value=["Column1", "Column2"],
            description="Columns",
        )

        default_years_subset = df.index.unique()[:4].tolist()
        self.years_subset_widget = widgets.SelectMultiple(
            options=df.index.unique().tolist(),
            value=default_years_subset,
            description="Years",
        )

        self.scale_factor_widget = widgets.FloatSlider(
            value=0.02, min=0.0, max=1.0, step=0.01, description="Scale Factor"
        )

        self.show_original_widget = widgets.Checkbox(
            value=True, description="Show Original"
        )

        self.growth_rate_widget = widgets.FloatSlider(
            value=0.02, min=0.0, max=1.0, step=0.01, description="Growth Rate"
        )

        self.moving_average_widget = widgets.Checkbox(
            value=False, description="Show Moving Average"
        )

        self.moving_average_window_widget = widgets.IntSlider(
            value=3, min=1, max=3, description="Moving Average Window"
        )

        self.plot_options_widgets = [
            widgets.Checkbox(value=False, description="Original + Moving Average"),
            widgets.Checkbox(value=False, description="Scaled on Original"),
            widgets.Checkbox(value=True, description="Growth Rate Moving Average"),
            widgets.Checkbox(value=True, description="Growth Rate on Original"),
        ]

        self.apply_conversion_widget = widgets.Checkbox(
            value=False, description="Apply Conversion"
        )

        self.convert_series_widget = widgets.Dropdown(
            options=scale_factor_df.index.tolist(),
            value="",  # Default value is an empty string
            description="Convert Series",
            style={"description_width": "initial"},
        )

        self.update_button = widgets.Button(description="Update Plot")
        self.update_button.on_click(self.update_plot)

        # Set up the event handler for the widget changes
        self.columns_subset_widget.observe(self.update_plot, names="value")
        self.years_subset_widget.observe(self.update_plot, names="value")
        self.scale_factor_widget.observe(self.update_plot, names="value")
        self.show_original_widget.observe(self.update_plot, names="value")
        self.growth_rate_widget.observe(self.update_plot, names="value")
        self.moving_average_widget.observe(self.update_plot, names="value")
        self.moving_average_window_widget.observe(self.update_plot, names="value")
        self.apply_conversion_widget.observe(self.update_plot, names="value")
        self.convert_series_widget.observe(self.update_plot, names="value")

        for option_widget in self.plot_options_widgets:
            option_widget.observe(self.update_plot, names="value")

        # Display the widgets and button
        display(
            self.columns_subset_widget,
            self.years_subset_widget,
            self.scale_factor_widget,
            self.show_original_widget,
            self.growth_rate_widget,
            self.moving_average_widget,
            self.moving_average_window_widget,
            *self.plot_options_widgets,
            self.apply_conversion_widget,
            self.convert_series_widget,
            self.update_button,
            self.output,
        )

    def update_plot(self, change=None):
        with self.output:
            clear_output(wait=True)  # Clear previous output
            columns_subset = self.columns_subset_widget.value
            years_subset = self.years_subset_widget.value
            scale_factor = self.scale_factor_widget.value
            show_original = self.show_original_widget.value
            growth_rate = self.growth_rate_widget.value
            moving_average = self.moving_average_widget.value
            moving_average_window = (
                self.moving_average_window_widget.value if moving_average else None
            )
            plot_original_moving_average = self.plot_options_widgets[0].value
            plot_scaled_on_original = self.plot_options_widgets[1].value
            plot_growth_rate_moving_average = self.plot_options_widgets[2].value
            plot_growth_rate_on_original = self.plot_options_widgets[3].value
            apply_conversion = self.apply_conversion_widget.value
            convert_series = self.convert_series_widget.value

            # Update the DataFrame based on the selected scale factor
            updated_df = self.df.copy()
            factor = (
                self.scale_factor_df.loc[convert_series]["factor"]
                if apply_conversion
                else 0.0
            )
            if factor and (factor != 0.0):
                updated_df = (updated_df * 1000) * (1 / factor)

            # Replace TimeSeriesPlotter with your actual class/method for plotting
            ts_plotter = TimeSeriesPlotter(updated_df)
            ts_plotter.plot_interactive_time_series(
                columns_subset=list(columns_subset),
                years_subset=list(years_subset),
                scale_factor=scale_factor,
                show_original=show_original,
                growth_rate=growth_rate,
                moving_average_window=moving_average_window,
                plot_original_moving_average=plot_original_moving_average,
                plot_scaled_on_original=plot_scaled_on_original,
                plot_growth_rate_moving_average=plot_growth_rate_moving_average,
                plot_growth_rate_on_original=plot_growth_rate_on_original,
            )


class InteractiveTimeSeriesPlotter:
    """
    %matplotlib widget
    ts_plotter = TimeSeriesPlotter(df)
    # Assuming df and ts_plotter are already defined
    interactive_plotter = InteractiveTimeSeriesPlotter(ts_plotter, df)
    """

    def __init__(self, ts_plotter, df):
        self.ts_plotter = ts_plotter
        self.df = df

        # Get available columns and years from the DataFrame
        self.available_columns = df.columns.tolist()
        self.available_years = sorted(df.index.unique().tolist())

        # Initialize widgets
        self.columns_selector = widgets.SelectMultiple(
            options=self.available_columns,
            value=[self.available_columns[0]],
            description="Select Columns",
        )
        self.years_selector = widgets.SelectMultiple(
            options=self.available_years,
            value=[self.available_years[0]],
            description="Select Years",
        )
        self.growth_rates_sliders = {
            col: widgets.FloatSlider(
                value=0.0,
                min=0.0,
                max=5.0,
                step=0.01,
                description=f"Growth Rate ({col})",
            )
            for col in self.available_columns
        }
        self.show_original_checkbox = widgets.Checkbox(
            value=True, description="Show Original"
        )

        # Create button and output widgets
        self.plot_button = widgets.Button(description="Plot Time Series")
        self.output_plot = widgets.Output()

        # Set up event handlers
        self.plot_button.on_click(self.plot_time_series)

        # Display widgets
        display(self.columns_selector, self.years_selector)
        display(widgets.HBox(list(self.growth_rates_sliders.values())))
        display(self.show_original_checkbox)
        display(self.plot_button)
        display(self.output_plot)

    def plot_time_series(self, _):
        # Get selected values from widgets
        with self.output_plot:
            clear_output(wait=True)
        selected_columns = self.columns_selector.value
        selected_years = self.years_selector.value
        growth_rates_dict = {
            col: self.growth_rates_sliders[col].value for col in selected_columns
        }
        show_original = self.show_original_checkbox.value

        # Plot the time series
        with self.output_plot:
            self.ts_plotter.plot_multiple_time_series(
                columns_subset=selected_columns,
                years_subset=selected_years,
                growth_rates=growth_rates_dict,
                show_original=show_original,
            )


class TimeSeriesPlotterWithDistribution:
    """
    # Assuming ts_plotter is an instance of TimeSeriesPlotter
    %matplotlib widget
    ts_plotter = TimeSeriesPlotter(df)
    # Assuming df is your DataFrame and ts_plotter is already defined
    interactive_plotter = TimeSeriesPlotterWithDistribution(ts_plotter, df)
    """

    def __init__(self, ts_plotter, df):
        self.ts_plotter = ts_plotter

        # Get available columns and years from the DataFrame (replace df with your actual DataFrame)
        self.available_columns = df.columns.tolist()
        self.available_years = sorted(df.index.unique().tolist())

        # Initialize widgets
        self.columns_selector = widgets.SelectMultiple(
            options=self.available_columns,
            value=[self.available_columns[0]],
            description="Select Columns",
        )
        self.years_selector = widgets.SelectMultiple(
            options=self.available_years,
            value=[self.available_years[0]],
            description="Select Years",
        )
        self.plot_selector = widgets.Select(
            options=[
                "plot_time_series_with_distribution",
                "plot_area_under_curve",
                "plot_heatmap",
            ],
            value="plot_time_series_with_distribution",
            description="Select Plot Type",
        )
        self.growth_rate_slider = widgets.FloatSlider(
            value=0.05, min=0.0, max=1.0, step=0.01, description="Growth Rate"
        )
        self.plot_button = widgets.Button(description="Plot Time Series")
        self.output_plot = widgets.Output()

        # Set up event handlers
        self.plot_button.on_click(self.plot_time_series)

        # Display widgets
        display(
            self.columns_selector,
            self.years_selector,
            self.growth_rate_slider,
            self.plot_selector,
        )
        display(self.plot_button)
        display(self.output_plot)

    def plot_time_series(self, _):
        # Get selected values from widgets
        with self.output_plot:
            clear_output(wait=True)
        selected_columns = self.columns_selector.value
        selected_years = self.years_selector.value
        growth_rate_to_apply = self.growth_rate_slider.value
        plot_type = self.plot_selector.value

        if plot_type == "plot_time_series_with_distribution":
            with self.output_plot:
                self.ts_plotter.plot_time_series_with_distribution(
                    column_subset=list(selected_columns),
                    year_subset=list(selected_years),
                    growth_rate=growth_rate_to_apply,
                )
        elif plot_type == "plot_area_under_curve":
            with self.output_plot:
                self.ts_plotter.plot_area_under_curve(
                    column_subset=list(selected_columns),
                    year_subset=list(selected_years),
                    growth_rate=growth_rate_to_apply,
                )
        elif plot_type == "plot_heatmap":
            with self.output_plot:
                self.ts_plotter.plot_heatmap(
                    column_subset=list(selected_columns),
                    year_subset=list(selected_years),
                    growth_rate=growth_rate_to_apply,
                )


class InteractivePlotter:
    """
    # Example usage
    # Assuming df is your DataFrame and plotter is your TimeSeriesVisualizer
    # plotter = TimeSeriesVisualizer(df)
    interactive_plotter = InteractivePlotter(df)
    """

    def __init__(self, df, conversion_factor=""):
        if conversion_factor:
            self.df = (df * 1000) * (1 / conversion_factor)
        else:
            self.df = df
        self.plotter = TimeSeriesVisualizer(df)

        # Get available columns and years from the dataframe
        self.available_columns = list(self.df.columns)
        self.available_years = list(self.df.index)

        # Create widgets
        self.column_selector = widgets.SelectMultiple(
            options=self.available_columns,
            value=[self.available_columns[0]],
            description="Columns",
        )

        self.year_selector = widgets.SelectMultiple(
            options=self.available_years,
            value=[self.available_years[0]],
            description="Years",
        )

        self.method_selector = widgets.Dropdown(
            options=self.get_plotter_methods(),
            value=self.get_plotter_methods()[0],
            description="Method",
        )

        self.growth_value_input = widgets.FloatText(
            value=0.05, description="Growth Value"
        )

        self.plot_button = widgets.Button(description="Plot")
        self.plot_button.on_click(self.plot)

        self.output_plot = widgets.Output()

        # Display widgets
        display(
            self.column_selector,
            self.year_selector,
            self.method_selector,
            self.growth_value_input,
            self.plot_button,
            self.output_plot,
        )

    def get_plotter_methods(self):
        # Get the names of the methods in the plotter class
        return [
            method
            for method in dir(self.plotter)
            if callable(getattr(self.plotter, method))
            and (not method.startswith("__"))
            and (not method.startswith("calculate"))
        ]

    def plot(self, _):
        with self.output_plot:
            # Clear previous output
            clear_output(wait=True)

            # Get selected values from widgets
            selected_columns = list(self.column_selector.value)
            selected_years = list(self.year_selector.value)
            selected_method = self.method_selector.value
            growth_value = self.growth_value_input.value

            # Call the selected method with the chosen parameters
            method_to_call = getattr(self.plotter, selected_method)

            if selected_method in ["plot_horizontal_bar_subplots"]:
                method_to_call(
                    columns=selected_columns,
                    years=selected_years,
                    growth_rate=growth_value,
                )
            else:
                method_to_call(columns=selected_columns, years=selected_years)
