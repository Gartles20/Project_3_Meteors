Meteorite Landings- A Full-stack Data Application Project

Project Overview-
  The purpose of this project was to take a meteorite landing dataset and create a full-stack data application. We are hoping to accomplish this by making data      visualizations which the user can manipulate to learn more about meteorite landings.
   
 Table of Contents
 https://github.com/Gartles20/Project_3_Meteors
 
 - [Project Structure](#project-structure)
 - [Data Description](#data-description)
 - [Research Questions](#research-questions)
 - [Data Application](#data-application)
 - [Conclusion](#conclusion)
 
 Project Structure
 The project directory structure is as follows:

 - │── Database/
 -  │ ├── .virtual_documents/
 - │ ├── Create_Database.ipynb
 - │ ├── cleaned_meteorite_data.csv
 - │ ├── meteorites.sqlite
 - │ ├── test_queries.ipynb
 - │ ├── test_visualizations.ipynb
 - │── app/
 - │ ├── static/
 - │├── templates/
 - │ ├── app.py
 - │ ├── meteorites.sqlite
 - │ ├── sql_helper.py
 - │── .DS_Store
 - │── .gitignore
 - │── LICENSE
 - │── Project 3 Proposal.pdf
 - │── Project 3 Writeup.pdf
 - │── Project_3_Meteors_Slides.pdf
 - │── README.md
 
Data Description
 Data and Cleaning Process:
 The dataset, sourced from Kaggle (pre-cleaned by Jay Panderson), underwent several cleaning
 steps:
 
   - The "year" column was converted from float to integer.
   - Rows with missing (NaN) values were removed.
   - Unnecessary or repetitive columns (e.g., name_type, location_type, fall, unnamed,
     geo_location) were dropped.
   
 The resulting dataset used in this project includes the following columns:
 1. Id: The number id given to the meteorite.
 2. rec_class: The class type of the meteorite.
 3. mass: The size of the meteorite in (g).
 4. year : The year the meteorite landed on Earth.
 5. rec_lat: The latitude coordinates of the landing site.
 6. rec_long: The longitude coordinates of the landing site.
    
 Example Queries
 1. To filter the data by the year and how many meteorites landed at that time.
       query = text("""SELECT
               year,
               count(id) as num_meteors
               FROM
               meteorites
               GROUP BY
               year
               ORDER BY
               year desc;""")
                         
 2. To filter the data by number of meteorites and class.
      query = f"""SELECT
              rec_class,
              COUNT() AS num_meteorites
              FROM meteorites
              GROUP BY rec_class
              HAVING COUNT() > 100;""")
    
 Research Questions
 
 1. Impact Patterns: Is there a geographic pattern to where meteorites are more likely to hit?
 2. Strike Frequency: How many meteor strikes occur within specific time frames?
 3. Meteor Classification: Which meteor class encounters Earth most frequently?
 
 Data Application
 Home Page
  ![Home page](https://github.com/user-attachments/assets/0eb3d474-a577-4207-8685-7918bdeeabf6)

 Plotly Dashboard
 
 Data Table -
  Data set with a filter start and ending year from 0-2013. You can look at all the different
   categories from the dataset.
 
 ![Data table png](https://github.com/user-attachments/assets/ef890c51-c464-4ee6-9786-448f20cd4968)

 Sunburst Chart-
   A sunburst chart that takes the year that the data was filtered by, and gives a visualization to
   see how many meteors of a specific class fell in that time frame.
![Sunburst Chart](https://github.com/user-attachments/assets/e94b25e7-fb59-4a3a-b23f-39a64c4e1d4c)

 Bar Graph- The bar graph shows the top 15 classes of meteorites that fell within the filtered time frame.
![Bar raph](https://github.com/user-attachments/assets/cfc6b5ff-c2f8-47d0-aa42-116a7df43b39)

Map Dashboard
 An interactive map where users can zoom in and see how where meteorites have fallen. There
 is a filter based on start and end year from 0 to 2013. There is also a heat map included that
 displays what geographic areas have been hit more frequently.

![Map Dashboard](https://github.com/user-attachments/assets/dd354820-bd91-41ca-81e1-f47ccdfad3e7)

About Us Page - To learn more about the creators of the website.

![About Us Page](https://github.com/user-attachments/assets/73d9c079-fcc3-4aa9-9bf3-9bbb64927b99)

 Works Cited - Referencing our sources
![Works cited](https://github.com/user-attachments/assets/d31522ea-10a9-4b39-903f-adb522dcebbc)

 Conclusion
 
 Impact Patterns: 
       The dashboard indicates that the eastern hemisphere is more frequently
       impacted by meteorites, with consistent results even when filtering data over the past 100
       years.
 
 Strike Frequency: 
       Between 1950 and 2013, there were 15,251 recorded meteorite landings. Users can explore different time periods using the interactive filters.
 
 Meteor Classification: 
      The most common meteorite class observed was L6 from the years of 1950 and 2013.
      
 Data Limitations:
 - The dataset is not current (data only up to 2013), which limits the app’s relevance for
 recent meteorite activity.
 - Visualization challenges arise with larger time frames due to data volume.
 
 Reporting Biases:
 - Human-reported data tends to over-represent meteorite strikes in populated areas.
 - Geographic factors make meteorites easier to spot in flat regions (e.g., deserts,
 Antarctica), possibly skewing the recorded data.
