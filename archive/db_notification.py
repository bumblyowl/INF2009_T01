import streamlit as st
import mysql.connector
from mysql.connector import Error
import time
from plyer import notification


# Function to count rows in the MySQL table
def count_rows(connection):
    query = "SELECT COUNT(*) FROM test"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except Error as e:
        st.error(f"Error counting rows in MySQL table: {e}")
        return None


# Function to establish a connection to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='proj',
            user='root',
            password='password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Streamlit App",
        timeout=10  # Notification timeout in seconds
    )

# Main function to run the Streamlit app
def main():
    # Connect to MySQL database
    connection = connect_to_database()
    # Initialize previous row count
    prev_row_count = count_rows(connection)

    # Main loop to count rows and trigger notification on increase
    while True:
        # Connect to MySQL database
        connection = connect_to_database()

        # Count rows in the MySQL table
        num_rows = count_rows(connection)

        # Print the current number of rows
        if num_rows is not None:
            print(f"Current number of rows in the table: {num_rows}")

            # Check for increase in row count
            if num_rows > prev_row_count:
                print("Number of rows increased!")
                prev_row_count = num_rows  # Update previous row count

                # Trigger notification
                send_notification("One row added to database", "This is a notification from the Streamlit app")

            # else:
            # st.write("No change in row count.")
        else:
            print("Failed to retrieve row count from the table.")

        # Close the connection
        if connection:
            connection.close()

        # Wait for 5 seconds before checking again
        time.sleep(3)


# Run the Streamlit app
if __name__ == "__main__":
    main()
