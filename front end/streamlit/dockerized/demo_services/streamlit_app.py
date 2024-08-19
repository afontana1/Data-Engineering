import streamlit as st
import pandas as pd
from file_loader import widget_process
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)

with col1:
    st.title("No-Code Analytics service by Databracket")
    st.header("Youtube: @data_bracket")
    st.header("Newsletter: databracket.substack.com")
with col2:
    st.image("databracket.png")

file_loader = widget_process()

def describe_df(df):
    st.write(df.describe())

def load_df(df):
    st.write(df)

def inspect_df(df):

    result = pd.DataFrame({
        'is_unique': df.nunique() == len(df),
        'cardinality': df.nunique(),
        'with_null': df.isna().any(),
        'missing_values': df.isnull().sum(),
        '1st_row': df.iloc[0],
        'last_row': df.iloc[-1],
        'dtype': df.dtypes
    })
    st.write(result)

try:
    sns.set(rc={'figure.figsize':(20,10)})
    dataframe = file_loader.read_file()
    # df = pd.read_csv(dataframe)
    @st.cache_data
    def read_csv(_dataframe):
        df = pd.read_csv(_dataframe)
        return df
    
    df = read_csv(_dataframe=dataframe)

    if df is not None:
        st.header("File to Dataframe")
        load = st.checkbox("Load")
        if load:
            load_df(df)

        st.header("Dataframe Description")
        describe = st.checkbox("Describe")
        if describe:
            describe_df(df)

        st.header("Dataframe Stats Inspection")
        Inspect = st.checkbox("Inspect")
        if Inspect:
            inspect_df(df)

        

        st.header("Select columns to plot")
        columns = list(df.columns.values)
        selected_columns = st.multiselect('Column Selection', columns)

        st.header("Choose which plot/graph you want to visualize")
        check1, check2, check3, check4 = st.columns(4)

        col1, col2, col3 = st.columns(3)

        cols = [col1, col2, col3]

        

        with check1:        
            hist = st.checkbox("Load Hist Plots")
        
        if hist:
            st.header("Hist Plot")
            if len(selected_columns) != 0:
                [1,2,3,4,5,6,7,8,9]
                
                sliced_cols = []
                for i in range(0, len(selected_columns), 3): 
                    col_chunk = selected_columns[i:i+3]
                    sliced_cols.append(col_chunk)

                for x in sliced_cols:
                    for j in range(len(x)):
                        with cols[j]:
                            fig, ax = plt.subplots()
                            ax.hist(df[x[j]], bins=20)
                            ax.set_title(x[j])

                            st.pyplot(fig)

        with check2:
            box = st.checkbox("Load Box Plots")

        if box:
            if len(selected_columns) != 0:
                st.write("box Plot")
                sliced_cols = []
                for i in range(0, len(selected_columns), 3): 
                    col_chunk = selected_columns[i:i+3]
                    sliced_cols.append(col_chunk)

                for x in sliced_cols:
                    for j in range(len(x)):
                        with cols[j]:
                            fig, ax = plt.subplots()
                            ax.boxplot(df[x[j]])
                            ax.set_title(x[j])

                            st.pyplot(fig)

        with check3:
            line = st.checkbox("Line chart")

        if line:
            st.line_chart(df[selected_columns])

        with check4:
            pair = st.checkbox("Pair plot")

        if pair:
            fig = sns.pairplot(data=df[selected_columns])

            st.pyplot(fig)
            # fig, ax = plt.subplots()
            # ax.pairplot(df)
            # ax.set_title('Pair Plot')

            # st.pyplot(fig)

        # if len(selected_columns) == 1:
        #     print(selected_columns[0])
        # elif len(selected_columns) == 2:
        #     print(selected_columns[0], selected_columns[1])
        # else:
        #     print("Multiple columns selected")

except UnboundLocalError:
    pass

