# Weather Analysis using sqlalchemy

##  Weather Analysis
- Analyzed weather data to plan a holiday vacation in Honolulu, Hawaii

### Step 1 - Climate Analysis and Exploration

To begin, used Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. Performed the following analysis using SQLAlchemy ORM queries, Pandas, and Matplotlib.

- Used the provided starter notebook and hawaii.sqlite files to complete your climate analysis and data exploration.
- Chose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.
- Used SQLAlchemy create_engine to connect to your sqlite database.
- Used SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

#### Precipitation Analysis

- Designed a query to retrieve the last 12 months of precipitation data.
- Selected only the date and prcp values.
- Loaded the query results into a Pandas DataFrame and set the index to the date column.
- Sorted the DataFrame values by date.
- Plotted the results using the DataFrame plot method.
- Used Pandas to print the summary statistics for the precipitation data.

#### Station Analysis

- Designed a query to calculate the total number of stations.
- Designed a query to find the most active stations.
- Listed the stations and observation counts in descending order.
- Designed a query to retrieve the last 12 months of temperature observation data (TOBS).
- Filtered by the station with the highest number of observations.
- Plotted the results as a histogram with bins=12.

### Step 2 - Climate App

- Used Flask to create the following routes:

1) Home page.
  - List all routes that are available.
  
2) /api/v1.0/precipitation
  - Convert the query results to a dictionary using date as the key and prcp as the value.
  - Return the JSON representation of your dictionary.
  
3)  /api/v1.0/stations
  - Return a JSON list of stations from the dataset.
  
4) /api/v1.0/tobs
  - Query the dates and temperature observations of the most active station for the last year of data.
  - Return a JSON list of temperature observations (TOBS) for the previous year.
  
5) /api/v1.0/<start> and /api/v1.0/<start>/<end>
  - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  - When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
  - When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

  

