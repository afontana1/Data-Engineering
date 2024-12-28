# Standard library imports
import os
import sqlite3
import threading
import time
from functools import wraps
import re
from datetime import datetime, timedelta

# Third-party imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy.stats import t
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage
from fuzzywuzzy import fuzz
import itertools
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Local imports
from src.api_model import EragAPI
from src.settings import settings
from src.look_and_feel import error, success, warning, info, highlight
from src.print_pdf import PDFReportGenerator
from src.helper_da import get_technique_info

class TimeoutException(Exception):
    pass

class AdvancedExploratoryDataAnalysisB6:
    def __init__(self, worker_erag_api, supervisor_erag_api, db_path):
        self.worker_erag_api = worker_erag_api
        self.supervisor_erag_api = supervisor_erag_api
        self.db_path = db_path
        self.technique_counter = 0
        self.total_techniques = 15
        self.table_name = None
        self.output_folder = None
        self.text_output = ""
        self.pdf_content = []
        self.findings = []
        self.llm_name = f"Worker: {self.worker_erag_api.model}, Supervisor: {self.supervisor_erag_api.model}"
        self.toc_entries = []
        self.image_paths = []
        self.max_pixels = 400000
        self.timeout_seconds = 10
        self.image_data = []
        self.pdf_generator = None
        self.settings = settings

    def calculate_figure_size(self, aspect_ratio=16/9):
        max_width = int(np.sqrt(self.max_pixels * aspect_ratio))
        max_height = int(max_width / aspect_ratio)
        return (max_width / 100, max_height / 100)

    def timeout(timeout_duration):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                result = [TimeoutException("Function call timed out")]

                def target():
                    try:
                        result[0] = func(self, *args, **kwargs)
                    except Exception as e:
                        result[0] = e

                thread = threading.Thread(target=target)
                thread.start()
                thread.join(timeout_duration)

                if thread.is_alive():
                    print(f"Warning: {func.__name__} timed out after {timeout_duration} seconds. Skipping this graphic.")
                    return None
                else:
                    if isinstance(result[0], Exception):
                        raise result[0]
                    return result[0]
            return wrapper
        return decorator

    @timeout(10)
    def generate_plot(self, plot_function, *args, **kwargs):
        return plot_function(*args, **kwargs)

    def get_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [table[0] for table in cursor.fetchall()]

    def run(self):
        print(info(f"Starting Advanced Exploratory Data Analysis (Batch 6) on {self.db_path}"))
        
        tables = self.get_tables()
        for table in tables:
            self.analyze_table(table)
        
        
        self.save_text_output()
        self.generate_pdf_report()
        # Remove this line:
        # self.save_unsuccessful_techniques()
        print(success(f"Advanced Exploratory Data Analysis (Batch 6) completed. Results saved in {self.output_folder}"))

    def analyze_table(self, table_name):
        self.table_name = table_name
        self.output_folder = os.path.join(settings.output_folder, f"axda_b6_{self.table_name}")
        os.makedirs(self.output_folder, exist_ok=True)
        
        self.pdf_generator = PDFReportGenerator(self.output_folder, self.llm_name, self.table_name)
        
        print(highlight(f"\nAnalyzing table: {table_name}"))
        self.text_output += f"\nAnalyzing table: {table_name}\n"
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

        analysis_methods = [
            self.trend_analysis,
            self.variance_analysis,
            self.regression_analysis,
            self.stratification_analysis,
            self.gap_analysis,
            self.duplicate_detection,
            self.process_mining,
            self.data_validation_techniques,
            self.risk_scoring_models,
            self.fuzzy_matching,
            self.continuous_auditing_techniques,
            self.sensitivity_analysis,
            self.scenario_analysis,
            self.monte_carlo_simulation,
            self.kpi_analysis
        ]

        for method in analysis_methods:
            try:
                method(df, table_name)
            except Exception as e:
                error_message = f"An error occurred during {method.__name__}: {str(e)}"
                print(error(error_message))
                self.text_output += f"\n{error_message}\n"
                self.pdf_content.append((method.__name__, [], error_message))
            finally:
                self.technique_counter += 1

    
    def trend_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Trend Analysis"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        date_cols = df.select_dtypes(include=['datetime64']).columns
        
        if len(date_cols) == 0 or len(numeric_cols) == 0:
            print(warning("No suitable columns for trend analysis."))
            return
        
        date_col = date_cols[0]
        df = df.sort_values(by=date_col)
        
        def plot_trend():
            fig, ax = plt.subplots(figsize=self.calculate_figure_size())
            for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
                ax.plot(df[date_col], df[col], label=col)
            ax.set_title('Trend Analysis')
            ax.set_xlabel('Date')
            ax.set_ylabel('Value')
            ax.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig, ax

        result = self.generate_plot(plot_trend)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_trend_analysis.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
            
            # Calculate trend statistics
            trend_stats = {}
            for col in numeric_cols:
                trend_stats[col] = {
                    'start': df[col].iloc[0],
                    'end': df[col].iloc[-1],
                    'change': df[col].iloc[-1] - df[col].iloc[0],
                    'percent_change': ((df[col].iloc[-1] - df[col].iloc[0]) / df[col].iloc[0]) * 100
                }
            
            self.interpret_results("Trend Analysis", {
                'image_paths': image_paths,
                'trend_stats': trend_stats
            }, table_name)
        else:
            print("Skipping Trend Analysis plot due to timeout.")

    def variance_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Variance Analysis"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print(warning("No numeric columns for variance analysis."))
            return
        
        variance_stats = df[numeric_cols].var()
        
        def plot_variance():
            fig, ax = plt.subplots(figsize=self.calculate_figure_size())
            variance_stats.plot(kind='bar', ax=ax)
            ax.set_title('Variance Analysis')
            ax.set_xlabel('Columns')
            ax.set_ylabel('Variance')
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig, ax

        result = self.generate_plot(plot_variance)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_variance_analysis.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
            
            self.interpret_results("Variance Analysis", {
                'image_paths': image_paths,
                'variance_stats': variance_stats.to_dict()
            }, table_name)
        else:
            print("Skipping Variance Analysis plot due to timeout.")

    def regression_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Regression Analysis"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print(warning("Not enough numeric columns for regression analysis."))
            return
        
        # Perform simple linear regression for each pair of numeric columns
        regression_results = {}
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                X = df[col1].values.reshape(-1, 1)
                y = df[col2].values
                model = LinearRegression()
                model.fit(X, y)
                r_squared = model.score(X, y)
                
                regression_results[f"{col1} vs {col2}"] = {
                    'r_squared': r_squared,
                    'coefficient': model.coef_[0],
                    'intercept': model.intercept_
                }
                
                def plot_regression():
                    fig, ax = plt.subplots(figsize=self.calculate_figure_size())
                    ax.scatter(X, y, alpha=0.5)
                    ax.plot(X, model.predict(X), color='red', linewidth=2)
                    ax.set_title(f'Regression: {col1} vs {col2}')
                    ax.set_xlabel(col1)
                    ax.set_ylabel(col2)
                    plt.tight_layout()
                    return fig, ax

                result = self.generate_plot(plot_regression)
                if result is not None:
                    fig, _ = result
                    img_path = os.path.join(self.output_folder, f"{table_name}_regression_{col1}_{col2}.png")
                    plt.savefig(img_path, dpi=100, bbox_inches='tight')
                    plt.close(fig)
                    image_paths.append(img_path)
                else:
                    print(f"Skipping Regression plot for {col1} vs {col2} due to timeout.")
        
        self.interpret_results("Regression Analysis", {
            'image_paths': image_paths,
            'regression_results': regression_results
        }, table_name)

    def stratification_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Stratification Analysis"))
        image_paths = []
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(categorical_cols) == 0 or len(numeric_cols) == 0:
            print(warning("No suitable columns for stratification analysis."))
            return
        
        stratification_results = {}
        for cat_col in categorical_cols[:2]:  # Limit to first 2 categorical columns
            for num_col in numeric_cols[:2]:  # Limit to first 2 numeric columns
                grouped = df.groupby(cat_col)[num_col].agg(['mean', 'median', 'std'])
                stratification_results[f"{cat_col} - {num_col}"] = grouped.to_dict()
                
                def plot_stratification():
                    fig, ax = plt.subplots(figsize=self.calculate_figure_size())
                    df.boxplot(column=num_col, by=cat_col, ax=ax)
                    ax.set_title(f'Stratification: {num_col} by {cat_col}')
                    ax.set_xlabel(cat_col)
                    ax.set_ylabel(num_col)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    return fig, ax

                result = self.generate_plot(plot_stratification)
                if result is not None:
                    fig, _ = result
                    img_path = os.path.join(self.output_folder, f"{table_name}_stratification_{cat_col}_{num_col}.png")
                    plt.savefig(img_path, dpi=100, bbox_inches='tight')
                    plt.close(fig)
                    image_paths.append(img_path)
                else:
                    print(f"Skipping Stratification plot for {cat_col} - {num_col} due to timeout.")
        
        self.interpret_results("Stratification Analysis", {
            'image_paths': image_paths,
            'stratification_results': stratification_results
        }, table_name)

    def gap_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Gap Analysis"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print(warning("No numeric columns for gap analysis."))
            return
        
        gap_results = {}
        for col in numeric_cols:
            current_value = df[col].mean()
            target_value = df[col].quantile(0.9)  # Using 90th percentile as target
            gap = target_value - current_value
            gap_percentage = (gap / target_value) * 100
            
            gap_results[col] = {
                'current_value': current_value,
                'target_value': target_value,
                'gap': gap,
                'gap_percentage': gap_percentage
            }
            
            def plot_gap():
                fig, ax = plt.subplots(figsize=self.calculate_figure_size())
                ax.bar(['Current', 'Target'], [current_value, target_value])
                ax.set_title(f'Gap Analysis: {col}')
                ax.set_ylabel('Value')
                plt.tight_layout()
                return fig, ax

            result = self.generate_plot(plot_gap)
            if result is not None:
                fig, _ = result
                img_path = os.path.join(self.output_folder, f"{table_name}_gap_analysis_{col}.png")
                plt.savefig(img_path, dpi=100, bbox_inches='tight')
                plt.close(fig)
                image_paths.append(img_path)
            else:
                print(f"Skipping Gap Analysis plot for {col} due to timeout.")
        
        self.interpret_results("Gap Analysis", {
            'image_paths': image_paths,
            'gap_results': gap_results
        }, table_name)

    def duplicate_detection(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Duplicate Detection"))
        image_paths = []
        
        duplicates = df.duplicated()
        duplicate_count = duplicates.sum()
        duplicate_percentage = (duplicate_count / len(df)) * 100
        
        duplicate_results = {
            'duplicate_count': duplicate_count,
            'duplicate_percentage': duplicate_percentage,
            'duplicate_rows': df[duplicates].to_dict(orient='records') if duplicate_count > 0 else []
        }
        
        def plot_duplicate_distribution():
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.calculate_figure_size())
            
            # Bar plot
            ax1.bar(['Unique', 'Duplicate'], [len(df) - duplicate_count, duplicate_count])
            ax1.set_title('Distribution of Unique vs Duplicate Rows')
            ax1.set_ylabel('Count')
            for i, v in enumerate([len(df) - duplicate_count, duplicate_count]):
                ax1.text(i, v, str(v), ha='center', va='bottom')
            
            # Pie chart
            ax2.pie([len(df) - duplicate_count, duplicate_count], 
                    labels=['Unique', 'Duplicate'], 
                    autopct='%1.1f%%', 
                    startangle=90)
            ax2.set_title('Proportion of Unique vs Duplicate Rows')
            
            plt.tight_layout()
            return fig, (ax1, ax2)

        result = self.generate_plot(plot_duplicate_distribution)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_duplicate_distribution.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        
        self.interpret_results("Duplicate Detection", {
            'image_paths': image_paths,
            'duplicate_results': duplicate_results
        }, table_name)

    def process_mining(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Process Mining"))
        image_paths = []
        
        # Assuming we have 'case_id', 'activity', and 'timestamp' columns
        required_cols = ['case_id', 'activity', 'timestamp']
        if not all(col in df.columns for col in required_cols):
            print(warning("Required columns for process mining not found."))
            return
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(['case_id', 'timestamp'])
        
        process_sequences = df.groupby('case_id')['activity'].agg(list)
        unique_sequences = process_sequences.value_counts()
        
        def plot_process_flow():
            fig, ax = plt.subplots(figsize=self.calculate_figure_size())
            unique_sequences.head(10).plot(kind='bar', ax=ax)
            ax.set_title('Top 10 Process Sequences')
            ax.set_xlabel('Process Sequence')
            ax.set_ylabel('Frequency')
            plt.xticks(rotation=90)
            plt.tight_layout()
            return fig, ax

        result = self.generate_plot(plot_process_flow)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_process_mining.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        else:
            print("Skipping Process Mining plot due to timeout.")
        
        process_mining_results = {
            'unique_sequences': unique_sequences.to_dict(),
            'total_cases': len(process_sequences),
            'average_activities_per_case': process_sequences.apply(len).mean()
        }
        
        self.interpret_results("Process Mining", {
            'image_paths': image_paths,
            'process_mining_results': process_mining_results
        }, table_name)

    def data_validation_techniques(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Data Validation Techniques"))
        
        validation_results = {
            'missing_values': df.isnull().sum().to_dict(),
            'negative_values': {col: (df[col] < 0).sum() for col in df.select_dtypes(include=[np.number]).columns},
            'out_of_range_values': {}
        }
        
        # Check for out of range values (assuming some reasonable ranges)
        for col in df.select_dtypes(include=[np.number]).columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            out_of_range = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            validation_results['out_of_range_values'][col] = out_of_range
        
        self.interpret_results("Data Validation Techniques", validation_results, table_name)

    def risk_scoring_models(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Risk Scoring Models"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print(warning("Not enough numeric columns for risk scoring model."))
            return
        
        # Simple risk scoring model: sum of normalized values
        scaler = MinMaxScaler()
        normalized_df = pd.DataFrame(scaler.fit_transform(df[numeric_cols]), columns=numeric_cols)
        risk_scores = normalized_df.sum(axis=1)
        
        # Define risk categories
        low_risk = (risk_scores <= risk_scores.quantile(0.5)).sum()
        medium_risk = ((risk_scores > risk_scores.quantile(0.5)) & (risk_scores <= risk_scores.quantile(0.9))).sum()
        high_risk = (risk_scores > risk_scores.quantile(0.9)).sum()
        
        def plot_risk_distribution():
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.calculate_figure_size())
            
            # Histogram
            risk_scores.hist(ax=ax1, bins=20)
            ax1.set_title('Distribution of Risk Scores')
            ax1.set_xlabel('Risk Score')
            ax1.set_ylabel('Frequency')
            
            # Pie chart
            ax2.pie([low_risk, medium_risk, high_risk], 
                    labels=['Low Risk', 'Medium Risk', 'High Risk'], 
                    autopct='%1.1f%%', 
                    startangle=90)
            ax2.set_title('Risk Categories Distribution')
            
            plt.tight_layout()
            return fig, (ax1, ax2)

        result = self.generate_plot(plot_risk_distribution)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_risk_distribution.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        else:
            print("Skipping Risk Distribution plot due to timeout.")
        
        risk_scoring_results = {
            'average_risk_score': risk_scores.mean(),
            'median_risk_score': risk_scores.median(),
            'high_risk_threshold': risk_scores.quantile(0.9),
            'high_risk_count': high_risk,
            'medium_risk_count': medium_risk,
            'low_risk_count': low_risk
        }
        
        self.interpret_results("Risk Scoring Models", {
            'image_paths': image_paths,
            'risk_scoring_results': risk_scoring_results
        }, table_name)

    def fuzzy_matching(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Fuzzy Matching"))
        image_paths = []
        
        text_cols = df.select_dtypes(include=['object']).columns
        
        if len(text_cols) == 0:
            print(warning("No text columns for fuzzy matching."))
            return
        
        fuzzy_results = {}
        for col in text_cols:
            unique_values = df[col].unique()
            if len(unique_values) > 100:  # Limit to prevent long processing times
                unique_values = unique_values[:100]
            
            matches = []
            for i, val1 in enumerate(unique_values):
                for val2 in unique_values[i+1:]:
                    ratio = fuzz.ratio(str(val1), str(val2))
                    if ratio > 80:  # Consider as a match if similarity > 80%
                        matches.append((val1, val2, ratio))
            
            fuzzy_results[col] = matches
        
        def plot_fuzzy_matches():
            fig, ax = plt.subplots(figsize=self.calculate_figure_size())
            match_counts = [len(matches) for matches in fuzzy_results.values()]
            ax.bar(fuzzy_results.keys(), match_counts)
            ax.set_title('Fuzzy Matches per Column')
            ax.set_xlabel('Columns')
            ax.set_ylabel('Number of Fuzzy Matches')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return fig, ax

        result = self.generate_plot(plot_fuzzy_matches)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_fuzzy_matches.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        
        self.interpret_results("Fuzzy Matching", {
            'image_paths': image_paths,
            'fuzzy_results': fuzzy_results
        }, table_name)

    def continuous_auditing_techniques(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Continuous Auditing Techniques"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print(warning("No numeric columns for continuous auditing."))
            return
        
        audit_results = {}
        for col in numeric_cols:
            audit_results[col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'outliers': len(df[(np.abs(stats.zscore(df[col])) > 3)])
            }
        
        def plot_outliers():
            fig, ax = plt.subplots(figsize=self.calculate_figure_size())
            outlier_counts = [results['outliers'] for results in audit_results.values()]
            ax.bar(audit_results.keys(), outlier_counts)
            ax.set_title('Outliers per Column')
            ax.set_xlabel('Columns')
            ax.set_ylabel('Number of Outliers')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return fig, ax

        result = self.generate_plot(plot_outliers)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_continuous_auditing_outliers.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        
        self.interpret_results("Continuous Auditing Techniques", {
            'image_paths': image_paths,
            'audit_results': audit_results
        }, table_name)

    def sensitivity_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Sensitivity Analysis"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print(warning("Not enough numeric columns for sensitivity analysis."))
            return
        
        # Perform simple sensitivity analysis: impact of 10% change in each variable
        baseline = df[numeric_cols].mean()
        sensitivity_results = {}
        
        for col in numeric_cols:
            changed = baseline.copy()
            changed[col] *= 1.1  # 10% increase
            impact = (changed - baseline) / baseline * 100
            sensitivity_results[col] = impact.to_dict()
        
        def plot_sensitivity():
            fig, ax = plt.subplots(figsize=self.calculate_figure_size())
            sns.heatmap(pd.DataFrame(sensitivity_results), annot=True, cmap='coolwarm', ax=ax)
            ax.set_title('Sensitivity Analysis: Impact of 10% Increase')
            plt.tight_layout()
            return fig, ax

        result = self.generate_plot(plot_sensitivity)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_sensitivity_analysis.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        else:
            print("Skipping Sensitivity Analysis plot due to timeout.")
        
        self.interpret_results("Sensitivity Analysis", {
            'image_paths': image_paths,
            'sensitivity_results': sensitivity_results
        }, table_name)

    def scenario_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Scenario Analysis"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print(warning("No numeric columns for scenario analysis."))
            return
        
        # Define scenarios
        scenarios = {
            'Baseline': 1.0,
            'Optimistic': 1.2,
            'Pessimistic': 0.8
        }
        
        scenario_results = {}
        for scenario, factor in scenarios.items():
            scenario_results[scenario] = (df[numeric_cols] * factor).mean().to_dict()
        
        def plot_scenario_comparison():
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.calculate_figure_size())
            
            # Bar plot
            scenario_sums = [sum(vals.values()) for vals in scenario_results.values()]
            ax1.bar(scenarios.keys(), scenario_sums)
            ax1.set_title('Scenario Comparison')
            ax1.set_ylabel('Sum of Averages')
            
            # Pie chart
            ax2.pie(scenario_sums, 
                    labels=scenarios.keys(), 
                    autopct='%1.1f%%', 
                    startangle=90)
            ax2.set_title('Scenario Distribution')
            
            plt.tight_layout()
            return fig, (ax1, ax2)

        result = self.generate_plot(plot_scenario_comparison)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_scenario_comparison.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        else:
            print("Skipping Scenario Comparison plot due to timeout.")
        
        self.interpret_results("Scenario Analysis", {
            'image_paths': image_paths,
            'scenario_results': scenario_results
        }, table_name)

    def monte_carlo_simulation(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - Monte Carlo Simulation"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print(warning("No numeric columns for Monte Carlo simulation."))
            return
        
        # Perform simple Monte Carlo simulation
        n_simulations = 1000
        simulation_results = {}
        
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            simulations = np.random.normal(mean, std, n_simulations)
            simulation_results[col] = {
                'mean': np.mean(simulations),
                'median': np.median(simulations),
                '5th_percentile': np.percentile(simulations, 5),
                '95th_percentile': np.percentile(simulations, 95)
            }
            
            def plot_monte_carlo():
                fig, ax = plt.subplots(figsize=self.calculate_figure_size())
                ax.hist(simulations, bins=30)
                ax.set_title(f'Monte Carlo Simulation: {col}')
                ax.set_xlabel('Value')
                ax.set_ylabel('Frequency')
                plt.tight_layout()
                return fig, ax

            result = self.generate_plot(plot_monte_carlo)
            if result is not None:
                fig, _ = result
                img_path = os.path.join(self.output_folder, f"{table_name}_monte_carlo_{col}.png")
                plt.savefig(img_path, dpi=100, bbox_inches='tight')
                plt.close(fig)
                image_paths.append(img_path)
            else:
                print(f"Skipping Monte Carlo plot for {col} due to timeout.")
        
        self.interpret_results("Monte Carlo Simulation", {
            'image_paths': image_paths,
            'simulation_results': simulation_results
        }, table_name)

    def kpi_analysis(self, df, table_name):
        print(info(f"Performing test {self.technique_counter}/{self.total_techniques} - KPI Analysis"))
        image_paths = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print(warning("No numeric columns for KPI analysis."))
            return
        
        # Define some example KPIs
        kpis = {
            'Average': np.mean,
            'Median': np.median,
            'Standard Deviation': np.std,
            'Coefficient of Variation': lambda x: np.std(x) / np.mean(x) if np.mean(x) != 0 else np.nan
        }
        
        kpi_results = {}
        for col in numeric_cols:
            kpi_results[col] = {kpi: func(df[col]) for kpi, func in kpis.items()}
        
        def plot_kpis():
            fig, ax = plt.subplots(figsize=self.calculate_figure_size())
            sns.heatmap(pd.DataFrame(kpi_results).T, annot=True, cmap='YlGnBu', ax=ax)
            ax.set_title('KPI Analysis')
            plt.tight_layout()
            return fig, ax

        result = self.generate_plot(plot_kpis)
        if result is not None:
            fig, _ = result
            img_path = os.path.join(self.output_folder, f"{table_name}_kpi_analysis.png")
            plt.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            image_paths.append(img_path)
        else:
            print("Skipping KPI Analysis plot due to timeout.")
        
        self.interpret_results("KPI Analysis", {
            'image_paths': image_paths,
            'kpi_results': kpi_results
        }, table_name)

    def save_results(self, analysis_type, results):
        if not self.settings.save_results_to_txt:
            return  # Skip saving if the option is disabled

        results_file = os.path.join(self.output_folder, f"{analysis_type.lower().replace(' ', '_')}_results.txt")
        with open(results_file, "w", encoding='utf-8') as f:
            f.write(f"Results for {analysis_type}:\n")
            if isinstance(results, dict):
                for key, value in results.items():
                    if key != 'image_paths':
                        f.write(f"{key}: {value}\n")
            else:
                f.write(str(results))
        print(success(f"Results saved as txt file: {results_file}"))

    def interpret_results(self, analysis_type, results, table_name):
        technique_info = get_technique_info(analysis_type)

        if isinstance(results, dict) and "Numeric Statistics" in results:
            numeric_stats = results["Numeric Statistics"]
            categorical_stats = results["Categorical Statistics"]
            
            numeric_table = "| Statistic | " + " | ".join(numeric_stats.keys()) + " |\n"
            numeric_table += "| --- | " + " | ".join(["---" for _ in numeric_stats.keys()]) + " |\n"
            for stat in numeric_stats[list(numeric_stats.keys())[0]].keys():
                numeric_table += f"| {stat} | " + " | ".join([f"{numeric_stats[col][stat]:.2f}" for col in numeric_stats.keys()]) + " |\n"
            
            categorical_summary = "\n".join([f"{col}:\n" + "\n".join([f"  - {value}: {count}" for value, count in stats.items()]) for col, stats in categorical_stats.items()])
            
            results_str = f"Numeric Statistics:\n{numeric_table}\n\nCategorical Statistics:\n{categorical_summary}"
        elif isinstance(results, pd.DataFrame):
            results_str = f"DataFrame with shape {results.shape}:\n{results.to_string()}"
        elif isinstance(results, dict):
            results_str = "\n".join([f"{k}: {v}" for k, v in results.items() if k != 'image_paths'])
        else:
            results_str = str(results)

        # Add information about number of visualizations
        num_visualizations = len(results.get('image_paths', []))
        results_str += f"\n\nNumber of visualizations created: {num_visualizations}"

        # Save the results
        self.save_results(analysis_type, results)

        common_prompt = f"""
        Analysis type: {analysis_type}
        Table name: {table_name}

        Technique Context:
        {technique_info['context']}

        Results:
        {results_str}

        Interpretation Guidelines:
        {technique_info['guidelines']}
        """

        worker_prompt = f"""
        You are an expert data analyst providing insights on exploratory data analysis results. Your task is to interpret the following analysis results and provide a detailed, data-driven interpretation, focusing on discovering patterns and hidden insights. Avoid jargon.

        {common_prompt}

        Please provide a thorough interpretation of these results, highlighting noteworthy patterns, anomalies, or insights. Focus on aspects that would be valuable for business decisions and operational improvements. Always provide specific numbers and percentages.

        Structure your response in the following format:

        1. Analysis performed and Key Insights:
        [Briefly describe the analysis performed. List at least 2-3 important insights discovered, with relevant numbers and percentages. Provide detailed explanations for each insight.]

        2. Patterns and Trends:
        [Describe at least 2-3 significant patterns or trends observed in the data. Explain their potential significance.]

        3. Potential Issues:
        [Highlight any anomalies, unusual trends, or areas of concern. Mention at least 2-3 potential problems, red flags, audit findings, fraud cases always including relevant numbers and percentages.]

        Ensure your interpretation is comprehensive and focused on actionable insights. While you can be detailed, strive for clarity in your explanations. Use technical terms when necessary, but provide brief explanations for complex concepts.

        Interpretation:
        """

        worker_interpretation = self.worker_erag_api.chat([{"role": "system", "content": "You are an expert data analyst providing insights for business leaders and analysts. Respond in the requested format."}, 
                                                    {"role": "user", "content": worker_prompt}])

        supervisor_prompt = f"""
        You are an expert data analyst providing insights on exploratory data analysis results. Your task is to interpret the following analysis results and provide a detailed, data-driven interpretation.

        {common_prompt}

        Please provide a thorough interpretation of these results, highlighting noteworthy patterns, anomalies, or insights. Focus on the most important aspects that would be valuable for business operations and decision-making. Always provide specific numbers and percentages when discussing findings.
        If some data appears to be missing or incomplete, work with the available information without mentioning the limitations. Your goal is to extract as much insight as possible from the given data.
        Structure your response in the following format:
        1. Analysis:
        [Provide a detailed description of the analysis performed, including specific metrics and their values]
        2. Key Findings:
        [List the most important discoveries, always including relevant numbers and percentages]
        3. Implications:
        [Discuss the potential impact of these findings on business operations and decision-making]
        4. Operational Recommendations:
        [Suggest concrete operational steps or changes based on these results. Focus on actionable recommendations that can improve business processes, efficiency, or outcomes. Avoid recommending further data analysis.]
        Ensure your interpretation is concise yet comprehensive, focusing on actionable insights derived from the data that can be directly applied to business operations.

        Business Analysis:
        """

        

        supervisor_analysis = self.supervisor_erag_api.chat([
            {"role": "system", "content": "You are a senior business analyst providing insights based on data analysis results. Provide a concise yet comprehensive business analysis."},
            {"role": "user", "content": supervisor_prompt}
        ])

        combined_interpretation = f"""
        Data Analysis:
        {worker_interpretation.strip()}

        Business Analysis:
        {supervisor_analysis.strip()}
        """

        


        print(success(f"Combined Interpretation for {analysis_type}:"))
        print(combined_interpretation.strip())

        self.text_output += f"\n{combined_interpretation.strip()}\n\n"

        # Handle images for the PDF report
        image_data = []
        if isinstance(results, dict) and 'image_paths' in results:
            for img in results['image_paths']:
                if isinstance(img, tuple) and len(img) == 2:
                    image_data.append(img)
                elif isinstance(img, str):
                    image_data.append((analysis_type, img))

        # Prepare content for PDF report
        pdf_content = f"""
        # {analysis_type}

        ## Data Analysis
        {worker_interpretation.strip()}

        
        ## Business Analysis
        {supervisor_analysis.strip()}
        """

        self.pdf_content.append((analysis_type, image_data, pdf_content))

        # Extract important findings
        self.findings.append(f"{analysis_type}:")
        lines = combined_interpretation.strip().split('\n')
        for i, line in enumerate(lines):
            if line.startswith("1. Analysis performed and Key Insights:") or line.startswith("2. Key Findings:"):
                for finding in lines[i+1:]:
                    if finding.strip() and not finding.startswith(("2.", "3.", "4.")):
                        self.findings.append(finding.strip())
                    elif finding.startswith(("2.", "3.", "4.")):
                        break

        # Update self.image_data for the PDF report
        self.image_data.extend(image_data)



    def save_text_output(self):
        output_file = os.path.join(self.output_folder, "axda_b6_results.txt")
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(self.text_output)

    def generate_pdf_report(self):
        report_title = f"Advanced Exploratory Data Analysis (Batch 6) Report for {self.table_name}"
        
        # Ensure all image data is in the correct format
        formatted_image_data = []
        for item in self.pdf_content:
            analysis_type, images, interpretation = item
            if isinstance(images, list):
                for image in images:
                    if isinstance(image, tuple) and len(image) == 2:
                        formatted_image_data.append(image)
                    elif isinstance(image, str):
                        # If it's just a string (path), use the analysis type as the title
                        formatted_image_data.append((analysis_type, image))
            elif isinstance(images, str):
                # If it's just a string (path), use the analysis type as the title
                formatted_image_data.append((analysis_type, images))
        
        pdf_file = self.pdf_generator.create_enhanced_pdf_report(
            self.findings,
            self.pdf_content,
            formatted_image_data,  # Use the formatted image data
            filename=f"axda_b6_{self.table_name}_report",
            report_title=report_title
        )
        if pdf_file:
            print(success(f"PDF report generated successfully: {pdf_file}"))
            return pdf_file
        else:
            print(error("Failed to generate PDF report"))
            return None
