import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# HTML content as a string
html_content = """
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <style>

        h3 { 
            text-align: center; 
            color: white;

        } 

        .toast-buttons { 
            max-width: 700px; 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: center; 
            gap: 15px; 
            margin: 2em auto; 
        } 

        .toast-row { 
            display: flex; 
            justify-content: center; 

            padding: 1rem; 
            flex-wrap: wrap; 
        } 

        button.custom-toast { 
            padding: 0.5rem 1rem; 
            border: none; 
            color: #fff; 
            font-weight: 500; 
            border-radius: 5px; 
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.785); 
            cursor: pointer; 
            width: 150px; 
            margin: 0.5em; 
            transition: filter 0.2s ease-in-out, 
                        transform 0.3s ease-in-out; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            font-size: 1rem; 
            background-color: transparent; 
            outline: none; 
            background: #3498db; 
            color: #fff; 
        } 

        button.custom-toast:hover { 
            filter: brightness(0.9); 
        } 

        button.info-toast { 
            background-color: #3498db; 
        }

        .toast { 
            position: fixed; 
            top: 25px; 
            right: 30px; 
            max-width: 300px; 
            background: #fff; 
            padding: 0.5rem; 
            border-radius: 4px; 
            box-shadow: -1px 1px 10px rgba(0, 0, 0, 0.3); 
            z-index: 1023; 
            animation: slideInRight 0.3s ease-in-out forwards, 
                        fadeOut 0.5s ease-in-out forwards 3s; 
            transform: translateX(110%); 
        } 

        .toast.closing { 
            animation: slideOutRight 0.5s ease-in-out forwards; 
        } 

        .toast-progress { 
            position: absolute; 
            display: block; 
            bottom: 0; 
            left: 0; 
            height: 4px; 
            width: 100%; 
            background: #b7b7b7; 
            animation: toastProgress 3s ease-in-out forwards; 
        } 

        .toast-content-wrapper { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
        } 

        .toast-icon { 
            padding: 0.35rem 0.5rem; 
            font-size: 1.5rem; 
        } 

        .toast-message { 
            flex: 1; 
            font-size: 0.9rem; 
            color: #000000; 
            padding: 0.5rem; 
        } 

        .toast.toast-success { 
            background: #95eab8; 
        } 

        .toast.toast-success .toast-progress { 
            background-color: #2ecc71; 
        } 

        .toast.toast-danger { 
            background: #efaca5; 
        } 

        .toast.toast-danger .toast-progress { 
            background-color: #e74c3c; 
        } 

        .toast.toast-info { 
            background: #bddaed; 
        } 

        .toast.toast-info .toast-progress { 
            background-color: #3498db; 
        } 

        .toast.toast-warning { 
            background: #ead994; 
        } 

        .toast.toast-warning .toast-progress { 
            background-color: #f1c40f; 
        } 

        @keyframes slideInRight { 
            0% { 
                transform: translateX(110%); 
            } 

            75% { 
                transform: translateX(-10%); 
            } 

            100% { 
                transform: translateX(0%); 
            } 
        } 

        @keyframes slideOutRight { 
            0% { 
                transform: translateX(0%); 
            } 

            25% { 
                transform: translateX(-10%); 
            } 

            100% { 
                transform: translateX(110%); 
            } 
        } 

        @keyframes fadeOut { 
            0% { 
                opacity: 1; 
            } 

            100% { 
                opacity: 0; 
            } 
        } 

        @keyframes toastProgress { 
            0% { 
                width: 100%; 
            } 

            100% { 
                width: 0%; 
            } 
        } 
    </style>
</head> 
<body> 
    <div class="container"> 
        <h3>Toast Notification in HTML CSS JavaScript</h3> 
        <div class="toast-buttons"> 
            <div class="toast-row"> 
                <button type="button" class="custom-toast info-toast">Toast Notification</button> 
            </div> 
        </div> 
    </div> 
    <div class="toast-overlay" id="toast-overlay"></div> 
    <script>
        // JavaScript code goes here
        let icon = {
            info: '<span class="material-symbols-outlined">back posture</span>'
        };

        const showToast = (message = "Sample Message", toastType = "info", duration = 5000) => {
            if (!Object.keys(icon).includes(toastType))
                toastType = "info";

            let box = document.createElement("div");
            box.classList.add("toast", `toast-${toastType}`);
            box.innerHTML = ` <div class="toast-content-wrapper"> 
                                <div class="toast-icon">${icon[toastType]}</div> 
                                <div class="toast-message">${message}</div> 
                                <div class="toast-progress"></div> 
                            </div>`;
            duration = duration || 5000;
            box.querySelector(".toast-progress").style.animationDuration = `${duration / 1000}s`;

            let toastAlready = document.body.querySelector(".toast");
            if (toastAlready) {
                toastAlready.remove();
            }

            document.body.appendChild(box)
        };

        let information = document.querySelector(".custom-toast.info-toast");

        information.addEventListener("click",(e) => {
            e.preventDefault();
            showToast("Sit up straight!","posture",5000);
        });


    </script> 
</body> 
</html>
"""

# Render the HTML content
st.components.v1.html(html_content, height=200)
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

# Displaying the data for the entered username
if not username_data.empty:
    st.subheader(f'Data for username: {username_input}')
    for index, row in username_data.iterrows():
        st.subheader(f"Details for username: {row['username']}")
        # Display the image
        if row['image'] is not None:
            image_data = row['image']
            image = Image.open(BytesIO(image_data))
            st.image(image, caption=f"Image for username: {row['username']}", use_column_width=True)
        else:
            st.write("No image found for the specified username.")

        # Display the other columns
        df_without_image = row.drop('image')
        st.dataframe(df_without_image, width=800)

        # Gauge graph for posture score
        st.subheader('Duration Score Gauge:')
        posture_score = df1['duration'].mean()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=posture_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Duration Score"},
            gauge={'axis': {'range': [None, 100]},
                   'steps': [
                       {'range': [0, 50], 'color': "lightgray"},
                       {'range': [50, 70], 'color': "gray"},
                       {'range': [70, 100], 'color': "lightgreen"}],
                   'threshold': {
                       'line': {'color': "red", 'width': 4},
                       'thickness': 0.75,
                       'value': posture_score}}))
        st.plotly_chart(fig)

        # Line graph for working time
        st.subheader('Working Time Line Chart:')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df1['timeStart'], y=df1['duration'], mode='lines+markers', name='Working Time'))
        fig.update_layout(title='Working Time Over Time',
                          xaxis_title='Date',
                          yaxis_title='Working Time (hours)')
        st.plotly_chart(fig)
else:
    st.write(f"No data found for username: {username_input}")
