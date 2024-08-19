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


# If widgets are not rendering or interactivity is not working
# https://github.com/jupyterlab/jupyterlab/issues/12580

# using plotly
# https://saturncloud.io/blog/troubleshooting-plotly-chart-not-showing-in-jupyter-notebook/


class ThreeDPlotter:
    """Basic Usage
    Generate random data

    plotter = ThreeDPlotter( dataframe=df)
    plotter.plot_3d_bar(columns_to_include=['Column1', 'Column2'], years_subset=[2010, 2011, 2013, 2014], growth_rate=0.05)
    plotter.plot_3d_line(columns_to_include=['Column1', 'Column2', 'Column3'], add_average=True, scale_factor=None, growth_rate=0.05,  show_original=True, years_subset=None)
    plotter.plot_3d_stem(columns_to_include=['Column1', 'Column2', 'Column3'], add_average=False, scale_factor=None, show_original=True, years_subset=None, growth_rate=0.05)
    """

    def __init__(self, dataframe, kind="By Column"):
        self.dataframe = dataframe
        self.kind = kind

    def plot_3d_line(
        self,
        columns_to_include=None,
        add_average=False,
        scale_factor=None,
        growth_rate=None,
        show_original=False,
        years_subset=None,
    ):
        """
        Generate a 3D line plot of time series data.

        Parameters:
        - columns_to_include: list, optional
            List of column names to include in the plot. If None, all columns in the dataframe are included.
        - add_average: bool, optional
            If True, add a line for the average value of each column.
        - scale_factor: float, optional
            Factor to scale the values by. If None, no scaling is applied.
        - growth_rate: float, optional
            Compound growth rate to apply to the values. If provided, a growth rate line is added to the plot.
        - show_original: bool, optional
            If True, show the original values in addition to any scaled or growth rate values.
        - years_subset: list, optional
            List of years to include in the plot. If None, all years in the dataframe are included.

        Returns:
        None
        """
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")

        if years_subset is None:
            years_subset = self.dataframe.index

        if columns_to_include is None:
            columns_to_include = self.dataframe.columns

        for i, column in enumerate(columns_to_include):
            if column in self.dataframe.columns:
                values = self.dataframe[column].loc[years_subset].values

                if show_original:
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        values,
                        label=f"{column} Original",
                        linestyle="-",
                        color="green",
                    )

                if (growth_rate is not None) and (growth_rate != 0.0):
                    t = np.arange(len(years_subset))
                    growth_values = values * (1 + growth_rate) ** t
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        growth_values,
                        linestyle="-",
                        color="orange",
                    )  # label=f'{column} Growth Rate'

                if (scale_factor is not None) and (scale_factor != 0.0):
                    scaled_values = values * scale_factor
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        scaled_values,
                        linestyle="-",
                        color="blue",
                    )  # label=f'{column} Scaled'

                if add_average:
                    average_value = values.mean()
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        np.full_like(years_subset, average_value),
                        linestyle="--",
                        color="black",
                    )  # label=f'{column} Average'

        ax.set_xlabel("Year")
        ax.set_ylabel("Columns")
        ax.set_zlabel("Values")
        ax.set_title(f"{self.kind}")

        # Set y-axis ticks and labels using column names
        ax.set_yticks(np.arange(len(columns_to_include)))
        ax.set_yticklabels(columns_to_include)
        ax.legend(
            loc="upper left", bbox_to_anchor=(3.5, 3.5), bbox_transform=fig.transFigure
        )
        # ax.legend()
        plt.show()

    def plot_3d_bar(
        self,
        columns_to_include=None,
        scale_factor=None,
        show_original=False,
        years_subset=None,
        growth_rate=None,
    ):
        """
        Generate a 3D bar chart of time series data.

        Parameters:
        - columns_to_include: list, optional
            List of column names to include in the plot. If None, all columns in the dataframe are included.
        - scale_factor: float, optional
            Factor to scale the values by. If None, no scaling is applied.
        - show_original: bool, optional
            If True, show the original values in addition to any scaled or growth rate values.
        - years_subset: list, optional
            List of years to include in the plot. If None, all years in the dataframe are included.
        - growth_rate: float, optional
            Compound growth rate to apply to the values. If provided, a growth rate bar is added to the plot.

        Returns:
        None
        """
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")

        if years_subset is None:
            years_subset = self.dataframe.index

        if columns_to_include is None:
            columns_to_include = self.dataframe.columns

        values = np.array(self.dataframe[columns_to_include].loc[years_subset].values)

        xpos, ypos = np.meshgrid(
            range(len(years_subset)), range(len(columns_to_include)), indexing="ij"
        )
        xpos = xpos.ravel()
        ypos = ypos.ravel()
        zpos = np.zeros_like(xpos)

        dx = dy = 0.4  # Adjust the width of the bars
        dz_original = values.ravel()

        if (growth_rate is not None) and (growth_rate != 0.0):
            t = np.arange(len(years_subset))
            growth_values = values * (1 + growth_rate) ** t[:, np.newaxis]
            dz_growth = growth_values.ravel()

            colors_growth = cm.Paired(np.linspace(0, 1, len(columns_to_include)))

            for i, (column, color_growth) in enumerate(
                zip(columns_to_include, colors_growth)
            ):
                ax.bar3d(
                    xpos[i :: len(columns_to_include)],
                    ypos[i :: len(columns_to_include)] + dy,
                    zpos[i :: len(columns_to_include)],
                    dx,
                    dy,
                    dz_growth[i :: len(columns_to_include)],
                    shade=True,
                    color=color_growth,
                    label=f"{column} Growth Rate",
                )

        if (scale_factor is not None) and (scale_factor != 0.0):
            dz_scaled = values.ravel() * scale_factor
            colors_scaled = cm.Dark2(np.linspace(0, 1, len(columns_to_include)))

            for i, (column, color_scaled) in enumerate(
                zip(columns_to_include, colors_scaled)
            ):
                ax.bar3d(
                    xpos[i :: len(columns_to_include)],
                    ypos[i :: len(columns_to_include)] + dy,
                    zpos[i :: len(columns_to_include)],
                    dx,
                    dy,
                    dz_scaled[i :: len(columns_to_include)],
                    shade=True,
                    color=color_scaled,
                    label=f"{column} Scaled",
                )

        colors_original = cm.viridis(np.linspace(0, 1, len(columns_to_include)))

        for i, (column, color_original) in enumerate(
            zip(columns_to_include, colors_original)
        ):
            ax.bar3d(
                xpos[i :: len(columns_to_include)],
                ypos[i :: len(columns_to_include)],
                zpos[i :: len(columns_to_include)],
                dx,
                dy,
                dz_original[i :: len(columns_to_include)],
                shade=True,
                color=color_original,
                label=f"{column} Original",
            )

        ax.set_xlabel("Year")
        ax.set_ylabel("Columns")
        ax.set_zlabel("Values")
        ax.set_title(f"{self.kind}")

        ax.set_xticks(np.arange(len(years_subset)) + 0.4)
        ax.set_xticklabels(years_subset)
        ax.set_yticks(np.arange(len(columns_to_include)) + 0.4)
        ax.set_yticklabels(columns_to_include)

        ax.legend()
        plt.show()

    def plot_3d_stem(
        self,
        columns_to_include=None,
        add_average=False,
        scale_factor=None,
        show_original=False,
        years_subset=None,
        growth_rate=None,
    ):
        """
        Generate a 3D stem plot of time series data.

        Parameters:
        - columns_to_include: list, optional
            List of column names to include in the plot. If None, all columns in the dataframe are included.
        - add_average: bool, optional
            If True, add a line for the average value of each column.
        - scale_factor: float, optional
            Factor to scale the values by. If None, no scaling is applied.
        - show_original: bool, optional
            If True, show the original values in addition to any scaled or averaged values.
        - years_subset: list, optional
            List of years to include in the plot. If None, all years in the dataframe are included.
        - growth_rate: float, optional
            Compound growth rate to apply to the values. If provided, a growth rate line is added to the plot.

        Returns:
        None
        """
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")

        if years_subset is None:
            years_subset = self.dataframe.index

        if columns_to_include is None:
            columns_to_include = self.dataframe.columns

        for i, column in enumerate(columns_to_include):
            if column in self.dataframe.columns:
                values = self.dataframe[column].loc[years_subset].values

                if (growth_rate is not None) and (growth_rate != 0.0):
                    t = np.arange(len(years_subset))
                    growth_values = values * (1 + growth_rate) ** t
                    ax.stem(
                        years_subset,
                        np.full_like(years_subset, i),
                        growth_values,
                        label=f"{column} Growth Rate",
                        basefmt="k-",
                        linefmt="--",
                        markerfmt="o",
                    )

                if show_original:
                    ax.stem(
                        years_subset,
                        np.full_like(years_subset, i),
                        values,
                        label=f"{column} Original",
                        basefmt="k-",
                        linefmt="--",
                        markerfmt="o",
                    )

                if (scale_factor is not None) and (scale_factor != 0.0):
                    scaled_values = values * scale_factor
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        scaled_values,
                        label=f"{column} Scaled",
                        linestyle="-",
                        color="blue",
                        marker="o",
                    )

                if add_average:
                    average_value = values.mean()
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        np.full_like(years_subset, average_value),
                        linestyle="--",
                        color="red",
                        label=f"{column} Average",
                    )

        ax.set_xlabel("Year")
        ax.set_ylabel("Columns")
        ax.set_zlabel("Values")
        ax.set_title(f"{self.kind}")

        # Set y-axis ticks and labels using column names
        ax.set_yticks(np.arange(len(columns_to_include)))
        ax.set_yticklabels(columns_to_include)

        ax.legend()
        plt.show()


class SubPlot3DPlotter:
    """Plots Multiple timeseries 3d on subplots

    Basic Usage:
        from data_generators import data_for_3d

        df = data_for_3d(num_years = 50, num_cols = 5)
        plotter = SubPlot3DPlotter(df)
        plotter.Column1"
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def plot_3d_line(self, subset_columns=None, subset_years=None):
        # Apply optional subsets
        df = self.dataframe.copy()
        if subset_columns is not None:
            df = df[subset_columns]

        if subset_years is not None:
            df = df[df.index.isin(subset_years)]

        num_columns = len(df.columns)
        num_rows = (num_columns + 2) // 3

        # Adjust the number of columns based on the actual number of columns
        num_columns_to_plot = min(3, num_columns)

        # Create subplots
        fig, axes = plt.subplots(
            num_rows,
            num_columns_to_plot,
            figsize=(15, 5 * num_rows),
            subplot_kw={"projection": "3d"},
        )
        fig.suptitle("Interactive 3D Subplots of Time Series")

        for i, column in enumerate(df.columns):
            row_index = i // num_columns_to_plot
            col_index = i % num_columns_to_plot
            ax = axes[row_index, col_index] if num_rows > 1 else axes[col_index]

            times = df.index
            values = df[column]
            line = ax.plot(range(len(times)), [1] * len(df), values, label=column)

            ax.set_xlabel("Time")
            ax.set_xticks(range(len(times)))
            ax.set_xticklabels([str(time) for time in times], rotation=45)
            ax.set_yticks([1])
            ax.set_yticklabels([column])
            ax.set_zlabel("Value")
            ax.set_title(column)

            # Use mplcursors for interactive data labels
            mplcursors.cursor(line, hover=True).connect(
                "add",
                lambda sel: sel.annotation.set_text(f"{column}: {sel.target[2]:.2f}"),
            )

        # Adjust layout
        fig.tight_layout(rect=[0, 0, 1, 0.96])

        # Remove empty subplots if needed
        if num_columns % 3 != 0:
            for i in range(num_columns % 3, 3):
                fig.delaxes(axes[-1, i])

        # Show plot
        plt.show()


class Interactive3DPlot:
    """
    %matplotlib widget
    interactive_plotter = Interactive3DPlot(df, scale_factor_df)
    """

    def __init__(self, df, scale_factor_df):
        self.df = df
        self.scale_factor_df = scale_factor_df

        # Initialize widgets
        self.columns_widget = widgets.SelectMultiple(
            options=df.columns.tolist(),
            value=["Column1", "Column2"],
            description="Columns to Include",
        )

        self.years_widget = widgets.SelectMultiple(
            options=df.index.unique().tolist(),
            value=[2010, 2011, 2013, 2014],
            description="Years Subset",
        )

        self.growth_rate_widget = widgets.FloatSlider(
            value=0.05,
            min=0.0,
            max=0.1,
            step=0.01,
            description="Growth Rate",
            style={"description_width": "initial"},
        )

        self.scale_dataframe_checkbox = widgets.Checkbox(
            value=False, description="Scale DataFrame"
        )

        self.scale_factor_widget = widgets.Dropdown(
            options=scale_factor_df.index.tolist(),
            value="",  # Default scale factor index
            description="Scale Factor",
            style={"description_width": "initial"},
        )

        self.interactive_plot = widgets.interactive(
            self.update_plot,
            columns_to_include=self.columns_widget,
            years_subset=self.years_widget,
            growth_rate=self.growth_rate_widget,
            scale_dataframe=self.scale_dataframe_checkbox,
            scale_factor=self.scale_factor_widget,
        )

        # Attach the update_checkbox function to the checkbox's value attribute
        self.scale_dataframe_checkbox.observe(self.update_checkbox, names="value")

        # Display the interactive widget
        display(widgets.VBox([self.scale_dataframe_checkbox, self.interactive_plot]))

    def update_plot(
        self,
        columns_to_include,
        years_subset,
        growth_rate,
        scale_dataframe,
        scale_factor,
    ):
        # Scale all columns in the dataframe by the specified scale factor if the checkbox is selected
        factor = (
            self.scale_factor_df.loc[scale_factor]["factor"] if scale_dataframe else 0.0
        )
        scaled_df = self.df.copy()
        if (scale_dataframe) and (factor != 0.0):
            scaled_df = (scaled_df) * (1 / factor)
            plotter = ThreeDPlotter(dataframe=scaled_df, kind="scaled")
        else:
            plotter = ThreeDPlotter(dataframe=scaled_df)
        plotter.plot_3d_bar(
            columns_to_include=list(columns_to_include),
            years_subset=list(years_subset),
            growth_rate=growth_rate,
        )

    def update_checkbox(self, change):
        self.scale_factor_widget.layout.visibility = (
            "visible" if change["new"] else "hidden"
        )


class InteractiveLinePlot:
    """
    %matplotlib widget
    interactive_plot = InteractiveLinePlot(df, scale_factor_df)
    """

    def __init__(self, df, scale_factor_df):
        self.df = df
        self.scale_factor_df = scale_factor_df
        self.columns_widget_line = widgets.SelectMultiple(
            options=self.df.columns.tolist(),
            value=("Column1", "Column2", "Column3"),
            description="Columns to Include",
        )
        self.years_widget_line = widgets.SelectMultiple(
            options=self.df.index.unique().tolist(),
            value=[2010, 2011, 2013, 2014],
            description="Years Subset",
        )
        self.add_average_widget = widgets.Checkbox(
            value=True, description="Add Average"
        )
        self.scale_factor_widget = widgets.FloatSlider(
            value=None,  # Set your desired default value
            min=0.0,
            max=2.0,
            step=0.1,
            description="Scale Factor",
            style={"description_width": "initial"},
        )
        self.growth_rate_widget_line = widgets.FloatSlider(
            value=0.05,
            min=0.0,
            max=0.1,
            step=0.01,
            description="Growth Rate",
            style={"description_width": "initial"},
        )
        self.show_original_widget = widgets.Checkbox(
            value=True, description="Show Original"
        )
        self.convert_series = widgets.Dropdown(
            options=self.scale_factor_df.index.tolist(),
            value="",  # Default value is an empty string
            description="Convert Series",
            style={"description_width": "initial"},
        )
        self.convert_series_checkbox = widgets.Checkbox(
            value=False, description="Convert Series"
        )
        self.interactive_line_plot = widgets.interactive(
            self.update_line_plot,
            columns_to_include=self.columns_widget_line,
            years_subset=self.years_widget_line,
            add_average=self.add_average_widget,
            scale_factor=self.scale_factor_widget,
            growth_rate=self.growth_rate_widget_line,
            show_original=self.show_original_widget,
            convert_series=self.convert_series,
        )
        display(
            widgets.VBox(
                [
                    self.convert_series_checkbox,
                    self.convert_series,
                    self.interactive_line_plot,
                ]
            )
        )

        self.convert_series_checkbox.observe(
            self.update_convert_series_widget, names="value"
        )

    def update_line_plot(
        self,
        columns_to_include,
        years_subset,
        add_average,
        scale_factor,
        growth_rate,
        show_original,
        convert_series,
    ):
        # Convert the series in df based on the selected convert_series value

        factor = (
            self.scale_factor_df.loc[convert_series]["factor"]
            if convert_series
            else 0.0
        )
        scaled_df = self.df.copy()
        if (convert_series) and (factor != 0.0):
            scaled_df = (scaled_df) * (1 / factor)
            plotter = ThreeDPlotter(dataframe=scaled_df, kind="Scaled")
        else:
            plotter = ThreeDPlotter(dataframe=scaled_df)
        plotter.plot_3d_line(
            columns_to_include=columns_to_include,
            add_average=add_average,
            scale_factor=scale_factor,
            growth_rate=growth_rate,
            show_original=show_original,
            years_subset=list(years_subset),
        )

    def update_convert_series_widget(self, change):
        self.convert_series.layout.visibility = "visible" if change["new"] else "hidden"


class Interactive3DStemPlotter:
    """
    %matplotlib widget
    interactive_plotter = Interactive3DStemPlotter(df, scale_factor_df)
    """

    def __init__(self, df, scale_factor_df):
        self.df = df
        self.scale_factor_df = scale_factor_df
        self.create_widgets()
        self.create_callback()

    def create_widgets(self):
        # Define interactive widgets with default values
        self.columns_widget_stem = widgets.SelectMultiple(
            options=self.df.columns.tolist(),
            value=("Column1", "Column2", "Column3"),
            description="Columns to Include",
        )

        self.years_widget_stem = widgets.SelectMultiple(
            options=self.df.index.unique().tolist(),
            value=[2010, 2011, 2013, 2014],
            description="Years Subset",
        )

        self.add_average_widget_stem = widgets.Checkbox(
            value=False, description="Add Average"
        )

        self.scale_factor_widget_stem = widgets.FloatSlider(
            value=None,  # Set your desired default value
            min=0.0,
            max=2.0,
            step=0.1,
            description="Scale Factor",
            style={"description_width": "initial"},
        )

        self.show_original_widget_stem = widgets.Checkbox(
            value=True, description="Show Original"
        )

        self.growth_rate_widget_stem = widgets.FloatSlider(
            value=0.05,
            min=0.0,
            max=0.1,
            step=0.01,
            description="Growth Rate",
            style={"description_width": "initial"},
        )

        # Dropdown for converting series
        self.convert_series_stem = widgets.Dropdown(
            options=self.scale_factor_df.index.tolist(),
            value="",  # Default value is an empty string
            description="Convert Series",
            style={"description_width": "initial"},
        )

        # Checkbox for whether to use convert_series
        self.convert_series_checkbox_stem = widgets.Checkbox(
            value=False, description="Convert Series"
        )

        # Create an interactive widget for the 3D stem plot
        self.interactive_stem_plot = widgets.interactive(
            self.update_stem_plot,
            columns_to_include=self.columns_widget_stem,
            years_subset=self.years_widget_stem,
            add_average=self.add_average_widget_stem,
            scale_factor=self.scale_factor_widget_stem,
            show_original=self.show_original_widget_stem,
            growth_rate=self.growth_rate_widget_stem,
            convert_series=self.convert_series_stem,
        )

        # Display the interactive widget for the 3D stem plot
        display(
            widgets.VBox(
                [
                    self.convert_series_checkbox_stem,
                    self.convert_series_stem,
                    self.interactive_stem_plot,
                ]
            )
        )

    def update_stem_plot(
        self,
        columns_to_include,
        years_subset,
        add_average,
        scale_factor,
        show_original,
        growth_rate,
        convert_series,
    ):
        # Convert the series in df based on the selected convert_series value
        factor = (
            self.scale_factor_df.loc[convert_series]["factor"]
            if convert_series
            else 0.0
        )
        scaled_df = self.df.copy()
        if (convert_series) and (factor != 0.0):
            scaled_df = (scaled_df) * (1 / factor)
            plotter = ThreeDPlotter(dataframe=scaled_df, kind="Scaled")
        else:
            plotter = ThreeDPlotter(dataframe=self.df)
        plotter.plot_3d_stem(
            columns_to_include=columns_to_include,
            add_average=add_average,
            scale_factor=scale_factor,
            show_original=show_original,
            years_subset=list(years_subset),
            growth_rate=growth_rate,
        )

    def create_callback(self):
        # Define a function to update the visibility of the convert_series widget based on the checkbox
        def update_convert_series_widget_stem(change):
            self.convert_series_stem.layout.visibility = (
                "visible" if change["new"] else "hidden"
            )

        # Attach the update_convert_series_widget function to the checkbox's value attribute
        self.convert_series_checkbox_stem.observe(
            update_convert_series_widget_stem, names="value"
        )


class Interactive3DLinePlotter:
    """
    %matplotlib widget
    interactive_line_plotter = Interactive3DLinePlotter(df)
    """

    def __init__(self, df):
        self.df = df
        self.create_widgets()
        self.create_callback()

    def create_widgets(self):
        # Define interactive widgets with default values
        self.columns_widget_line = widgets.SelectMultiple(
            options=self.df.columns.tolist(),
            value=self.df.columns.tolist(),
            description="Columns to Include",
        )

        self.years_widget_line = widgets.SelectMultiple(
            options=self.df.index.unique().tolist(),
            value=self.df.index.unique()[:3].tolist(),
            description="Years Subset",
        )

        # Create an interactive widget for the 3D line plot
        self.interactive_line_plot = widgets.interactive(
            self.update_line_plot,
            subset_columns=self.columns_widget_line,
            subset_years=self.years_widget_line,
        )

        # Display the interactive widget for the 3D line plot
        display(self.interactive_line_plot)

    def update_line_plot(self, subset_columns, subset_years):
        plotter = SubPlot3DPlotter(self.df)
        plotter.plot_3d_line(
            subset_columns=list(subset_columns),
            subset_years=list(subset_years) if subset_years else None,
        )

    def create_callback(self):
        # Define a function to update the options of the years widget based on the selected columns
        def update_years_options(change):
            selected_columns = change["new"]
            all_years = self.df.index.unique().tolist()

            # If no columns are selected, display all years
            if not selected_columns:
                self.years_widget_line.options = all_years
                return

            # Display only the years that have data for the selected columns
            available_years = self.df[selected_columns].dropna().index.unique().tolist()
            self.years_widget_line.options = available_years

        # Attach the update_years_options function to the columns widget's value attribute
        self.columns_widget_line.observe(update_years_options, names="value")
