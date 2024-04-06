import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from streamlit_modal import Modal
import mysql.connector
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
from io import BytesIO

# Define custom CSS for adjusting component width
custom_css = """ 
<style> 
/* Define width for the page */ 
.stApp { 
    max-width: 100%; 
} 

/* Define width for the page component */ 
.stPage > div > div > div > div { 
    width: 90%; 
} 
</style> 
"""

# Write the custom CSS
st.write(custom_css, unsafe_allow_html=True)

# Your Streamlit app content
st.title("Streamlit App")

# Establish connection to the database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="proj"
)

# Create a cursor object to execute SQL queries
cursor = db_connection.cursor()

# Define the SQL query to fetch data from the test table
select_query = "SELECT username, timeStart, duration, eyeDist, image FROM test"

# Execute the SQL query
cursor.execute(select_query)

# Fetch all rows of the result
rows = cursor.fetchall()

# Close the cursor
cursor.close()

# Close the database connection
db_connection.close()

# Convert the fetched rows into a DataFrame
columns = ['username', 'timeStart', 'duration', 'eyeDist', 'image']
df1 = pd.DataFrame(rows, columns=columns)

# Convert the 'timeStart' column to string format
df1['timeStart'] = df1['timeStart'].astype(str)
# Displaying the data from the test table
st.subheader('Data from MySQL Test Table:')

# Text input for username
username_input = st.text_input("Enter username:")
username_data = df1[df1['username'] == username_input]


# Function to display modal
def display_modal(image_data, username, time_start, duration):
    key = f"image_modal_{username}_{time_start}_{duration}"
    modal = Modal(key=key, title="Test Modal")
    open_modal = st.button(label=f'Image at {time_start}')
    if open_modal:
        with modal.container():
            if image_data is not None:
                image = Image.open(BytesIO(image_data))
                st.image(image, caption="Image", use_column_width=None)
            else:
                st.write("No image found.")
# Displaying the data for the entered username
if not username_data.empty:
    # st.subheader(f'Data for username: {username_input}')
    # for index, row in username_data.iterrows():
    #     st.subheader(f"Details for username: {username_input}")
    #     #Display the image
    #     if row['image'] is not None:
    #         image_data = row['image']
    #         image = Image.open(BytesIO(image_data))
    #         st.image(image, caption=f"Image for username: {row['username']}", use_column_width=True)
    #     else:
    #         st.write("No image found for the specified username.")
    #
    #     #Display the other columns
    #     df_without_image = row.drop('image')
    #     st.dataframe(df_without_image, width=800)

    # Create a second DataFrame without the 'username' column
    df2 = username_data.copy()
    # Update the 'Modal Button' column with buttons that trigger the modal

    #st.write(df2, width=1000)
    # Create a new column in df2 to hold the buttons
    # Display the DataFrame
    col1, col2, col3, col4 = st.columns((5, 2, 2, 5))

    # Display column headers
    col1.write("Time Start")
    col2.write("Duration")
    col3.write("Eye Dist")
    col4.write("Image")

    # Iterate through DataFrame rows and display data
    for index, row in df2.iterrows():
        with col1:
            st.write(row['timeStart'])
        with col2:
            st.write(row['duration'])
        with col3:
            st.write(row['eyeDist'])
        with col4:  # Create an empty placeholder for buttons
            button_key = f"button_{index}"  # Generate unique key for the button
            display_modal(row['image'], row['username'], row['timeStart'], row['duration'])

    # Gauge graph for posture score
    st.subheader('Number of hours in a bad posture:')
    posture_score = (df1['duration'] / 60).mean()
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=posture_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Duration"},
        gauge={'axis': {'range': [None, 2]},
               'steps': [
                   {'range': [0, 0.5], 'color': "lightgreen"},
                   {'range': [0.5, 1], 'color': "yellow"},
                   {'range': [1, 1.5], 'color': "orange"},
                   {'range': [1.5, 2], 'color': "red"}],
               'threshold': {
                   'line': {'color': "blue", 'width': 4},
                   'thickness': 0.75,
                   'value': posture_score}}))
    st.plotly_chart(fig)

    # Convert 'timeStart' column to datetime
    df2['timeStart'] = pd.to_datetime(df2['timeStart'])

    # Extract date and time
    df2['Date'] = df2['timeStart'].dt.date
    df2['Time'] = df2['timeStart'].dt.time

    # Count unique dates
    unique_dates = df2['Date'].nunique()
    # Group by date and count rows
    daily_counts = df2.groupby('Date').size().reset_index(name='Count')
    unique_dates_list = df2['Date'].unique().tolist()
    # Convert unique dates to string format ("%Y-%m-%d") and sort them
    unique_dates_list_str = sorted([date.strftime("%Y-%m-%d") for date in unique_dates_list])

    # Line chart
    line_chart = go.Figure(go.Scatter(x=unique_dates_list_str, y=daily_counts['Count'], mode='lines+markers'))
    line_chart.update_layout(title='Number of Bad Posture per Day',
                             xaxis_title='Date',
                             yaxis_title='Number of Bad Posture',
                             xaxis=dict(
                                 tickmode='array',
                                 tickvals=unique_dates_list_str,
                                 dtick='M1'  # Set the tick interval to 1 month
                             ))
    st.plotly_chart(line_chart)


else:
    st.write(f"No data found for username: {username_input}")
