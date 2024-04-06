import mysql.connector
from PIL import Image
from io import BytesIO

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

# Define the SQL query to select the image data from the table
select_query = "SELECT image FROM your_table_name WHERE username = %s"
username = "sample_username"

# Execute the SQL query
cursor.execute(select_query, (username,))

# Fetch the result from the cursor
result = cursor.fetchone()

# Close the cursor and database connection
cursor.close()
db_connection.close()

# Check if result is not None and if there's data in it
if result is not None and result[0] is not None:
    # Decode the binary data
    image_data = result[0]
    
    # Open the image using PIL
    image = Image.open(BytesIO(image_data))
    
    # Display the image
    image.show()
else:
    print("No image found for the specified username.")