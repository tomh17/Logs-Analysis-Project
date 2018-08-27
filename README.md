# Logs-Analysis-Project
For Udacity course: Build a reporting tool that answers three questions provided by Udacity. 1. Which articles were the most popular 2. Which author had the most cumulative views 3. Which dates had error percentages above 1%

# Necessary Tools / Materials
 Vagrant VM as well as VirtualBox software donwloaded on machine.You will also need access the the "news" databse provided by Udacity.   The querying is done using postgreSQL as well python 3.7. 

You must create two views for this code to work properly. They are as follows:
1. CREATE VIEW all_connections AS SELECT substring(time::text, 0, 11)
AS DATE, COUNT(status) AS all FROM log GROUP BY date ORDER BY date DESC;
2.CREATE VIEW not_running AS SELECT substring(time::text, 0, 11) AS DATE,
COUNT(status) AS not_ok FROM log WHERE status='404 NOT FOUND' GROUP BY
date ORDER BY date DESC;

# Explanation of code for most_pop_articles():
Using psycopg2 we can connect to the database using DNname
db.cursor() allows python to exectue a postgreSQL command
Using c.execute, it calls the function 'cursor' and executes the sql command.
Within this function I created a SQL query that will display the
name of the articles along with the number of views each had
I did this by joining the "articles" and "log" tables and using CONCAT to make sure that "path" in log and "slug" in articles
matched. Then I grouped it by the name of the articles and ordered them by which article had the most connections
aka "views" on the log table. I then printed a name for the list that will be returned and then indented the results using \t, then the title article, then a hyphen to separate the article name from it's number of views.
In summary: the functions returns the title of the article as well as a count of all the times that the slug=path
aka everytime the article was viewed.

# Explanation of code for most_pop_authors()
Selects the author name and the title of each article every time the
slug+path match up as well as when the authors match up with their own articles (articles.author=authors.id) thus creating a
count of the number of times it was viewed cumulatively this is almost identical to the "most popular articles" function above
except that I added the "AND articles.author=authors.id"

# Explanation of code for error_dates():
For this function I needed to create two views. They are as follows:
CREATE VIEW all_connections AS SELECT substring(time::text, 0, 11)
AS DATE, COUNT(status) AS all FROM log GROUP BY date ORDER BY date DESC;
All connections: a view that lists all the dates in order by date
along with the number of views on each day (all = number of connections)
I used the substring function to only
incorporate the date (YYYY-MM-DD) into the table.

The second view I created is as follows:

CREATE VIEW not_running AS SELECT substring(time::text, 0, 11) AS DATE,
COUNT(status) AS not_ok FROM log WHERE status='404 NOT FOUND' GROUP BY
date ORDER BY date DESC;
This view displays the number of times the connections failed
aka where there was a "404 not found" error.
This view was also ordered by date allowing me to connect them in the SQL
query that I used in the function.
Using both views I combined their data into one table.
The query in the function above first converts the date within each table
from YYYY-MM-DD to Month Day, Year
it then selects both the number of errors from the "not_running" view
as well as the total number of connections from the "all_connections" view
and and divides them. From there, the WHERE command determines
which dates/ decimals will be displayed since it will only display
dates where the error percentage is greater than 1%.
Within the python code, I added a "%" to the end of the decimal so the
user sees it as a percentage. The ROUND function is used so that the
decimal produced only has two decimal places. 
