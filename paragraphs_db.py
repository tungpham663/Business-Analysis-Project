import psycopg2
from crawler import crawl
from extract_para import extract_paragraphs
import random

DB_HOST = "localhost"
DB_NAME = "testDB"
DB_USER = "postgres"
DB_PASSWORD = "tung060603"

# Database connection function
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error: Unable to connect to PostgreSQL - {str(e)}")
        return None

# Function to create a table if it doesn't exist
def create_table():
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS articles5 (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    date VARCHAR(10),
                    keyword VARCHAR(255)
                );
                """
                cursor.execute(create_table_query)
                conn.commit()
                print("Table created successfully or already exists.")
        except Exception as e:
            print(f"Error creating table: {str(e)}")
        finally:
            conn.close()

# Function to insert extracted data into the table
def insert_article(content, date, keyword):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO articles5 (content, date, keyword)
                VALUES (%s, %s, %s);
                """
                cursor.execute(insert_query, (content, date, keyword))
                conn.commit()
                print(f"Inserted: Content='{content}...', Date='{date}', Keyword='{keyword}'")
        except Exception as e:
            print(f"Error inserting data: {str(e)}")
        finally:
            conn.close()

# Main function to process and store all articles
def process_and_store_articles(articles):
    create_table()  # Ensure table exists
    for article in articles:
        content, date, keyword = extract_paragraphs(crawl(article))
        if content != "":
            for para in content:
                insert_article(para, date, keyword)

def search_samples_by_keyword(keyword):
    """
    Search for the 5 latest samples in the 'articles' table based on the keyword.

    Parameters:
        keyword (str): The keyword to search for.

    Returns:
        list: A list of dictionaries containing the matching samples.
    """
    query = """
    SELECT content, date, keyword
    FROM articles5
    WHERE keyword ILIKE %s
    ORDER BY TO_DATE(date, 'DD/MM/YYYY') DESC, id DESC
    LIMIT 10;
    """
    results = []

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with conn.cursor() as cursor:
            # Execute the query
            cursor.execute(query, (f"%{keyword}%",))
            rows = cursor.fetchall()
            
            # Convert query results to a list of dictionaries
            for row in rows:
                results.append({
                    "content": row[0],
                    "date": row[1],
                    "keyword": row[2]
                })
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()
    
    if results:
        return random.choice(results)['content']
    else:
        return ''
    
def check_keyword_in_db(keyword):
    """
    Check if the given keyword exists in the 'articles' table in the database.

    Parameters:
        keyword (str): The keyword to search for.

    Returns:
        bool: True if the keyword exists, False otherwise.
    """
    query = """
    SELECT EXISTS (
        SELECT 1
        FROM articles
        WHERE keyword ILIKE %s
    );
    """
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with conn.cursor() as cursor:
            # Execute the query with the keyword parameter
            cursor.execute(query, (f"%{keyword}%",))
            exists = cursor.fetchone()[0]  # Fetch the boolean result
        
        return exists  # True if exists, False otherwise

    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        # Close the connection
        if conn:
            conn.close()