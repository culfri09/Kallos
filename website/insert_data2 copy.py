import psycopg2
from psycopg2 import OperationalError

try:
    # Connect to existing database
    conn = psycopg2.connect(
        database="postgres",
        user="docker",
        password="docker",
        host="127.0.0.1",
        port="5432"  # Specify port for PostgreSQL
    )

    print("Connection successful!")

    # Open cursor to perform database operation
    cur = conn.cursor()

    # Query to list all table names
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
    table_rows = cur.fetchall()
    tables = [row[0] for row in table_rows]  # Extract table names from the fetched rows

    print("List of tables:")
    for table in tables:
        print(table)

    #============CREATE NEW RECORD=============

     # SQL command to insert a row into the User table
    sql_command = """
        INSERT INTO \"Kallos_Users\" (id, email, password, first_name, company_name, job_title, department)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Data to be inserted into the table
    data = (
        2,  # id
        'casandara@example.com',  # email
        'casandra',  # password
        'casandra',  # first_name
        'Acme Corporation',  # company_name
        'Software Engineer',  # job_title
        'qa'  # department
    )

    # Execute the SQL command with the data
    cur.execute(sql_command, data)

    # Commit the transaction
    conn.commit()

    print("Insert operation successful!")


    #===============LIST DATA FROM KALLOS USERS ==================

    # SQL command to list all data in the Kallos_Users table
    sql_command = "SELECT * FROM \"Kallos_Users\";"


    # Execute the SQL command
    cur.execute(sql_command)

    # Fetch all rows
    rows = cur.fetchall()

    # Print the data
    print("Data in Kallos_Users table:")
    for row in rows:
        print(row)

    # Close communications with database
    cur.close()
    conn.close()

except OperationalError as e:
    print(f"Connection failed: {e}")
