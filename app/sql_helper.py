from sqlalchemy import create_engine, text
import pandas as pd
import os

class SQLHelper:
    def __init__(self):
        # Get the absolute path to the current directory
        base_dir = os.path.abspath(os.path.dirname(__file__))
        # Join it with the database file name
        db_path = os.path.join(base_dir, 'meteorites.sqlite')
        self.engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

    #################################################################

    def query_meteorite_counts(self, min_year):
        """Query meteorite counts grouped by class."""
        query = text("""
            SELECT rec_class, COUNT(*) as count, Year as year
            FROM meteorites
            WHERE Year >= :min_year
            GROUP BY rec_class
        """)
        return self._execute_query(query, {"min_year": min_year})

    #################################################################

    def query_data(self, min_year):
        """Query meteorite data filtered by year."""
        query = text("""
            SELECT
                Year as year,
                rec_class as class,
                mass as mass,
                rec_lat as latitude,
                rec_long as longitude
            FROM meteorites
            WHERE Year >= :min_year
            ORDER BY Year ASC;
        """)
        return self._execute_query(query, {"min_year": min_year})

    #################################################################

    def map_data(self, min_year):
        """Query for map data, limiting the number of results to improve performance."""
        query = text("""
            SELECT 
                rec_lat, 
                rec_long, 
                AVG(mass) AS avg_mass, 
                COUNT(*) AS num_meteorites
            FROM meteorites
            WHERE year >= COALESCE(:min_year, 0)
            GROUP BY rec_lat, rec_long
            ORDER BY num_meteorites DESC
            LIMIT 1000;  -- Limit results to prevent slow performance
        """)
        return self._execute_query(query, {"min_year": min_year})

    #################################################################

    def sunburst_data(self, min_year):
        """Get data for a sunburst chart."""
        query1 = text("""
            WITH TopYears AS (
                SELECT Year
                FROM meteorites
                GROUP BY Year
                ORDER BY COUNT(*) DESC
                LIMIT 15
            ),
            TopClasses AS (
                SELECT rec_class, Year, COUNT(*) AS count,
                    ROW_NUMBER() OVER (PARTITION BY Year ORDER BY COUNT(*) DESC) AS rank
                FROM meteorites
                WHERE Year IN (SELECT Year FROM TopYears)
                GROUP BY rec_class, Year
            )
            SELECT rec_class AS label, count, Year AS parent
            FROM TopClasses
            WHERE rank <= 10
            ORDER BY Year, count DESC;
        """)
        df1 = self._execute_query(query1, {"min_year": min_year})

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
        df2 = self._execute_query(query2, {"min_year": min_year})

        # Add parent column to df2 and combine
        df2["parent"] = ""
        df = pd.concat([df1, df2], ignore_index=True)
        return df

    #################################################################

    def _execute_query(self, query, params=None):
        """Executes a query safely while keeping the connection stable."""
        with self.engine.connect() as conn:
            return pd.read_sql(query, con=conn, params=params)




    




    

