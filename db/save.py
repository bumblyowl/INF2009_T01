import mysql.connector

# Establish connection to the database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="transzh",
    port=3307
)

# Create a cursor object to execute SQL queries
cursor = db_connection.cursor()

# Define the SQL query to insert data into the table
insert_query = "INSERT INTO your_table_name (username, timeStart, image, duration, eyeDist) VALUES (%s, %s, %s, %s, %s)"

# Sample data to insert
username = "sample_username"
timeStart = "12:00:00"

# Read the image data from file
with open("x.jpg", "rb") as image_file:
    image_data = image_file.read()

duration = 60
eyeDist = 5

# Execute the SQL query
cursor.execute(insert_query, (username, timeStart, image_data, duration, eyeDist))

# Commit the transaction
db_connection.commit()

# Close the cursor and database connection
cursor.close()
db_connection.close()
