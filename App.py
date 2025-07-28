import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
# Set the page configuration
st.set_page_config(page_title='Data Visualizer', layout='wide', page_icon='📊')

# Title of the app
st.title('📊 Data Visualizer')

# Function to download plot as PNG
def download_plot_as_png(fig, filename="plot.png"):
    """
    Generates a link to download a Matplotlib plot as a PNG file.
    """
    png_image = io.BytesIO()
    fig.savefig(png_image, format='png')
    png_image.seek(0)  # Rewind the data stream

    b64 = base64.b64encode(png_image.read()).decode('utf-8')
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">Download plot as PNG</a>'
    return href

# File upload and dataset selection
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = None

# Initialize session state variables if not already done
if 'x_axis' not in st.session_state:
    st.session_state.x_axis = None
if 'y_axis' not in st.session_state:
    st.session_state.y_axis = None
if 'plot_type' not in st.session_state:
    st.session_state.plot_type = None

# Sidebar with renamed options
option = st.sidebar.selectbox('Select Option', ['Individual Plot', 'Comparison Plots'])

if df is not None:
    if option == 'Individual Plot':
        st.header('Individual Plot')

        # Display the dataframe
        st.write(df.head())

        # Allow the user to select columns for plotting
        st.session_state.x_axis = st.selectbox('Select the X-axis', options=[''] + df.columns.tolist(), key='individual_x_axis')
        st.session_state.y_axis = st.selectbox('Select the Y-axis', options=[''] + df.columns.tolist(), key='individual_y_axis')

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 'Heatmap']
        st.session_state.plot_type = st.selectbox('Select the type of plot', options=plot_list, key='individual_plot_type')

        x_color = st.color_picker('Select Color for Graph', '#1f77b4')

        if st.button('Generate Plot'):
            try:
                if st.session_state.plot_type == 'Line Plot':
                    if st.session_state.x_axis and st.session_state.y_axis:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        sns.lineplot(x=df[st.session_state.x_axis], y=df[st.session_state.y_axis], ax=ax, color=x_color)
                        ax.tick_params(axis='x', labelsize=10)
                        ax.tick_params(axis='y', labelsize=10)
                        st.pyplot(fig)
                        download_link = download_plot_as_png(fig)
                        st.markdown(download_link, unsafe_allow_html=True)
                        st.subheader('Summary of the Graph')
                        st.write(f"The plot shows how {st.session_state.y_axis} changes with {st.session_state.x_axis}.")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**X-axis Summary:**")
                            st.write(df[st.session_state.x_axis].describe())
                        with col2:
                            st.write("**Y-axis Summary:**")
                            st.write(df[st.session_state.y_axis].describe())
                        correlation = df[[st.session_state.x_axis, st.session_state.y_axis]].corr().iloc[0, 1]
                        st.write(f"**Correlation between {st.session_state.x_axis} and {st.session_state.y_axis}:** {correlation:.2f}")
                    else:
                        st.error("Please select valid X-axis and Y-axis columns for the Line Plot.")

                elif st.session_state.plot_type == 'Scatter Plot':
                    if st.session_state.x_axis and st.session_state.y_axis:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        sns.scatterplot(x=df[st.session_state.x_axis], y=df[st.session_state.y_axis], ax=ax, color=x_color)
                        ax.tick_params(axis='x', labelsize=10)
                        ax.tick_params(axis='y', labelsize=10)
                        st.pyplot(fig)
                        download_link = download_plot_as_png(fig)
                        st.markdown(download_link, unsafe_allow_html=True)
                        st.subheader('Summary of the Graph')
                        st.write(f"The plot shows the relationship between {st.session_state.x_axis} and {st.session_state.y_axis}.")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**X-axis Summary:**")
                            st.write(df[st.session_state.x_axis].describe())
                        with col2:
                            st.write("**Y-axis Summary:**")
                            st.write(df[st.session_state.y_axis].describe())
                        correlation = df[[st.session_state.x_axis, st.session_state.y_axis]].corr().iloc[0, 1]
                        st.write(f"**Correlation between {st.session_state.x_axis} and {st.session_state.y_axis}:** {correlation:.2f}")
                    else:
                        st.error("Please select valid X-axis and Y-axis columns for the Scatter Plot.")

                elif st.session_state.plot_type == 'Bar Chart':
                    if st.session_state.x_axis and st.session_state.y_axis:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        sns.barplot(x=df[st.session_state.x_axis], y=df[st.session_state.y_axis], ax=ax, color=x_color)
                        ax.tick_params(axis='x', labelsize=10)
                        ax.tick_params(axis='y', labelsize=10)
                        st.pyplot(fig)
                        download_link = download_plot_as_png(fig)
                        st.markdown(download_link, unsafe_allow_html=True)
                        st.subheader('Summary of the Graph')
                        st.write(f"The plot compares the values of {st.session_state.y_axis} across different {st.session_state.x_axis} categories.")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**X-axis Summary:**")
                            st.write(df[st.session_state.x_axis].describe())
                        with col2:
                            st.write("**Y-axis Summary:**")
                            st.write(df[st.session_state.y_axis].describe())
                        correlation = df[[st.session_state.x_axis, st.session_state.y_axis]].corr().iloc[0, 1]
                        st.write(f"**Correlation between {st.session_state.x_axis} and {st.session_state.y_axis}:** {correlation:.2f}")
                    else:
                        st.error("Please select valid X-axis and Y-axis columns for the Bar Chart.")

                elif st.session_state.plot_type == 'Distribution Plot':
                    if st.session_state.x_axis:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        sns.histplot(df[st.session_state.x_axis], kde=True, ax=ax, color=x_color)
                        ax.set_xlabel(st.session_state.x_axis)
                        ax.set_ylabel('Density')
                        ax.tick_params(axis='x', labelsize=10)
                        ax.tick_params(axis='y', labelsize=10)
                        st.pyplot(fig)
                        download_link = download_plot_as_png(fig)
                        st.markdown(download_link, unsafe_allow_html=True)
                        st.subheader('Summary of the Graph')
                        st.write(f"The plot displays the distribution of {st.session_state.x_axis}.")
                        st.write("**X-axis Summary:**")
                        st.write(df[st.session_state.x_axis].describe())
                    else:
                        st.error("Please select a valid X-axis column for the Distribution Plot.")

                elif st.session_state.plot_type == 'Count Plot':
                    if st.session_state.x_axis:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        sns.countplot(x=df[st.session_state.x_axis], ax=ax, color=x_color)
                        ax.tick_params(axis='x', labelsize=10)
                        ax.tick_params(axis='y', labelsize=10)
                        st.pyplot(fig)
                        download_link = download_plot_as_png(fig)
                        st.markdown(download_link, unsafe_allow_html=True)
                        st.subheader('Summary of the Graph')
                        st.write(f"The plot counts the occurrences of each category in {st.session_state.x_axis}.")
                        st.write("**X-axis Summary:**")
                        st.write(df[st.session_state.x_axis].describe())
                    else:
                        st.error("Please select a valid X-axis column for the Count Plot.")

                elif st.session_state.plot_type == 'Heatmap':
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
                    ax.tick_params(axis='x', labelsize=10)
                    ax.tick_params(axis='y', labelsize=10)
                    st.pyplot(fig)
                    download_link = download_plot_as_png(fig)
                    st.markdown(download_link, unsafe_allow_html=True)
                    st.subheader('Summary of the Graph')
                    st.write("The plot displays the correlation matrix of the dataset.")
                    st.write("**Correlation Matrix:**")
                    st.write(df.corr())
                else:
                    st.error("Invalid plot type selected.")
            except Exception as e:
                st.error(f"An error occurred while generating the plot: {e}")

    elif option == 'Comparison Plots':
        st.header('Comparison Plots')

        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=[''] + df.columns.tolist(), key='comparison_x_axis')
        y_axis = st.selectbox('Select the Y-axis', options=[''] + df.columns.tolist(), key='comparison_y_axis')

        # Color picker for comparison plots
        color = st.color_picker('Select Color for Graph', '#1f77b4', key='comparison_color')

        if st.button('Generate Comparison Plots'):
            if x_axis and y_axis:
                plot_types = ['Line Plot', 'Scatter Plot', 'Bar Chart', 'Distribution Plot', 'Count Plot', 'Heatmap']
                colors = [color] * len(plot_types)  # Apply the same color to all plot types

                for plot_type in plot_types:
                    st.subheader(f'{plot_type} of {y_axis} vs {x_axis}')

                    try:
                        if plot_type == 'Line Plot':
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax, color=colors[0])
                        elif plot_type == 'Scatter Plot':
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax, color=colors[1])
                        elif plot_type == 'Bar Chart':
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax, color=colors[2])
                        elif plot_type == 'Distribution Plot':
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.histplot(df[x_axis], kde=True, ax=ax, color=colors[3])
                            ax.set_xlabel(x_axis)
                            ax.set_ylabel('Density')
                        elif plot_type == 'Count Plot':
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.countplot(x=df[x_axis], ax=ax, color=colors[4])
                        elif plot_type == 'Heatmap':
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', linewidths=.5, ax=ax)

                        # Set plot title
                        ax.set_title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=14)
                        ax.tick_params(axis='x', labelsize=10)
                        ax.tick_params(axis='y', labelsize=10)
                        st.pyplot(fig)

                        download_link = download_plot_as_png(fig, f"{plot_type}_{x_axis}_{y_axis}.png")
                        st.markdown(download_link, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"An error occurred while generating the {plot_type}: {e}")
            else:
                st.warning("Please select options for plotting.")
else:
    st.warning("Please upload a CSV file to proceed.")
