import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import mysql.connector
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
from io import BytesIO

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
select_query = "SELECT username, timeStart, duration, eyeDist FROM test"

# Execute the SQL query
cursor.execute(select_query)

# Fetch all rows of the result
rows = cursor.fetchall()

# Close the cursor
cursor.close()

# Close the database connection
db_connection.close()

# Convert the fetched rows into a DataFrame
columns = ['username', 'timeStart', 'duration', 'eyeDist']
df1 = pd.DataFrame(rows, columns=columns)

# Convert the 'timeStart' column to string format
df1['timeStart'] = df1['timeStart'].astype(str)
# Displaying the data from the test table
st.subheader('Data from MySQL Test Table:')

# Text input for username
username_input = st.text_input("Enter username:")
username_data = df1[df1['username'] == username_input]

# Displaying the data for the entered username
if not username_data.empty:
    st.subheader(f'Data for username: {username_input}')
    #for index, row in username_data.iterrows():
    #st.subheader(f"Details for username: {username_input}")
        # Display the image
        # if row['image'] is not None:
        #     image_data = row['image']
        #     image = Image.open(BytesIO(image_data))
        #     st.image(image, caption=f"Image for username: {row['username']}", use_column_width=True)
        # else:
        #     st.write("No image found for the specified username.")

        # Display the other columns
        #df_without_image = row.drop('image')
        #st.dataframe(df_without_image, width=800)

    # Create a second DataFrame without the 'username' column
    df2 = username_data.drop(columns=['username'])
    st.dataframe(df2, width=800)

    # Gauge graph for posture score
    st.subheader('Duration Score Gauge:')
    posture_score = (df1['duration'] / 60).mean()
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=posture_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Duration Score"},
        gauge={'axis': {'range': [None, 2]},
               'steps': [
                   {'range': [0, 0.5], 'color': "green"},
                   {'range': [0.5, 1], 'color': "yellow"},
                   {'range': [1, 1.5], 'color': "orange"},
                   {'range': [1.5, 2], 'color': "red"}],
               'threshold': {
                   'line': {'color': "pink", 'width': 4},
                   'thickness': 0.75,
                   'value': posture_score}}))
    st.plotly_chart(fig)

    df2['timeStart'] = pd.to_datetime(df2['timeStart'])

    # Group by day and count the number of rows
    daily_counts = df2.groupby(df2['timeStart'].dt.date).size().reset_index(name='count')

    # Line graph for number of rows per day
    st.subheader('Number of Rows per Day Line Chart:')
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=daily_counts['timeStart'], y=daily_counts['count'], mode='lines+markers', name='Number of Rows'))
    fig.update_layout(title='Number of Rows per Day',
                      xaxis_title='Date',
                      yaxis_title='Number of Rows',
                      xaxis=dict(
                          tickformat='%Y-%m-%d'  # Set the tick format to show only the date part
                      ))
    st.plotly_chart(fig)
else:
    st.write(f"No data found for username: {username_input}")
