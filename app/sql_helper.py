from sqlalchemy import create_engine, text
import pandas as pd
import os

class SQLHelper:
    def __init__(self):
        # Get the absolute path to the current directory
        base_dir = os.path.abspath(os.path.dirname(__file__))
        # Join it with the database file name
        db_path = os.path.join(base_dir, 'meteorites.sqlite')
        self.engine = create_engine(f"sqlite:///{db_path}")

    #################################################################

    def query_meteorite_counts(self, min_year):
        """Query meteorite counts grouped by class."""
        with self.engine.connect() as conn:
            query = text("""
                SELECT rec_class, COUNT(*) as count
                FROM meteorites
                WHERE
                    Year >= :min_year
                GROUP BY rec_class
            """)
            df = pd.read_sql(query, con=conn, params={"min_year": min_year})
        return df  # No need to manually close with `with` statement

    #################################################################

    def query_data(self, min_year):
        """Query meteorite data filtered by year."""
        with self.engine.connect() as conn:
            query = text("""
                SELECT
                    Year as year,
                    rec_class as class,
                    mass as mass,
                    rec_lat as latitude,
                    rec_long as longitude
                FROM
                    meteorites
                WHERE
                    Year >= :min_year
                ORDER BY
                    Year ASC;
            """)
            df = pd.read_sql(query, con=conn, params={"min_year": min_year})
        return df  # No need to manually close with `with` statement

    def map_data(self, min_year):
        with self.engine.connect() as conn:
            query = text("""
            SELECT 
                rec_lat, 
                rec_long, 
                mass, 
                COUNT(*) AS num_meteorites
            FROM meteorites
            WHERE (:min_year IS NULL OR year >= :min_year)
            GROUP BY rec_lat, rec_long, mass
            ORDER BY mass DESC;
        """)
        
        df = pd.read_sql(query, con=conn, params={"min_year": min_year})
    
        return df




    




    

