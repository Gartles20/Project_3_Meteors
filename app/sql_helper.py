from sqlalchemy import create_engine, text
import pandas as pd

# Define the SQLHelper Class
# PURPOSE: Deal with all of the database logic

import os
from sqlalchemy import create_engine

class SQLHelper():
    def __init__(self):
        # Get the absolute path to the current directory
        base_dir = os.path.abspath(os.path.dirname(__file__))
        # Join it with the database file name
        db_path = os.path.join(base_dir, 'meteorites.sqlite')
        self.engine = create_engine(f"sqlite:///{db_path}")


    #################################################################

    def query_meteorite_counts(self):
        # Create our session (link) from Python to the DB
        conn = self.engine.connect()  # Raw SQL/Pandas

        # Define Query
        query = text("""
            SELECT rec_class, COUNT(*) as count
            FROM meteorites
            GROUP BY rec_class
        """)
        
        # Execute the query and load the results into a DataFrame
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()

        # Return the DataFrame (or you can return rows if you prefer)
        return df
    
    def query_data(self, min_year):
        conn = self.engine.connect()  # Raw SQL/Pandas

        # Define Query
        query = text(f"""SELECT
                    Year as year,
                    rec_class as class,
                    mass as mass,
                    rec_lat as latitude,
                    rec_long as longitude
                FROM
                    meteorites
                WHERE
                    Year >= {min_year}
                ORDER BY
                    Year asc;""")
        
        # Execute the query and load the results into a DataFrame
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()

        # Return the DataFrame (or you can return rows if you prefer)
        return df


    




    

