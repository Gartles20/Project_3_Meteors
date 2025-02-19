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
                SELECT rec_class, COUNT(*) as count, Year as year
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

    def sunburst_data(self, min_year):
            with self.engine.connect() as conn:
            # Query for rec_class and year
                query1 = text("""
                        WITH TopYears AS (
                            SELECT Year
                            FROM meteorites
                            GROUP BY Year
                            ORDER BY COUNT(*) DESC
                            LIMIT 15
                        ),

                        -- Get the top 10 rec_class for each year
                        TopClasses AS (
                            SELECT rec_class, Year, COUNT(*) AS count,
                                ROW_NUMBER() OVER (PARTITION BY Year ORDER BY COUNT(*) DESC) AS rank
                            FROM meteorites
                            WHERE Year IN (SELECT Year FROM TopYears)
                            GROUP BY rec_class, Year
                        )

                        -- First query: Filtered rec_class breakdown by year
                        SELECT rec_class AS label, count, Year AS parent
                        FROM TopClasses
                        WHERE rank <= 10
                        ORDER BY Year, count DESC;
                """)
                df1 = pd.read_sql(query1, con=conn, params={"min_year": min_year})
                print("Query 1 Success:", df1.head())  # Debugging output

                # Query for year-level aggregation
                query2 = text("""
                    WITH TopYears AS (
                        SELECT Year
                        FROM meteorites
                        GROUP BY Year
                        ORDER BY COUNT(*) DESC
                        LIMIT 15
                    )
                    SELECT Year AS label, COUNT(*) AS count, '' AS parent
                    FROM meteorites
                    WHERE Year IN (SELECT Year FROM TopYears) AND Year >= :min_year
                    GROUP BY Year
                    ORDER BY count DESC;
                """)
                df2 = pd.read_sql(query2, con=conn, params={"min_year": min_year})
                print("Query 2 Success:", df2.head())  # Debugging output
            # Add parent column to df2
            df2["parent"] = ""
            # Combine DataFrames
            df = pd.concat([df1, df2], ignore_index=True)
            return df



    




    

