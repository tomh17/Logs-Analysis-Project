# Logs-Analysis-Project
For Udacity course: Build a reporting tool that answers three questions provided by Udacity. 1. Which articles were the most popular 2. Which author had the most cumulative views 3. Which dates had error percentages above 1%

# Necessary Tools / Materials
 Vagrant VM as well as VirtualBox software donwloaded on machine.You will also need access the the "news" databse provided by Udacity.   The querying is done using postgreSQL 9.5 as well python 3.7. 

Once you have acces to the "news" database and are in the correct vagrant directory you can type:

>psql news

And from there you can begin to work with the appropriate tables. 

You must create two views for this code to work properly. They are as follows:

>CREATE VIEW all_connections AS SELECT substring(time::text, 0, 11)
>AS DATE, COUNT(status) AS all FROM log GROUP BY date ORDER BY date DESC;

>CREATE VIEW not_running AS SELECT substring(time::text, 0, 11) AS DATE,
>COUNT(status) AS not_ok FROM log WHERE status='404 NOT FOUND' GROUP BY
>date ORDER BY date DESC;

# Running the Code

You must have the file saved on the Vagrant virtual machine with access to Udacity's "news" database. The code can be ran from the command line as follows:

> $ python3 logs_analysis1.py

# Explanation of code for most_pop_articles():
1. Using psycopg2 we can connect to the database using DNname
2. db.cursor() allows python to exectue a postgreSQL command
3. Using c.execute, it calls the function 'cursor' and executes the sql command.
   Within this function I created a SQL query that will display the
   name of the articles along with the number of views each had based on data in the "log" table.
4. I did this by joining the "articles" and "log" tables.
5. In order to join these tables I needed to adjust the "slug" data using CONCAT.  To make sure that "path" in log and "slug" in      articles matched. 

Reasoning for using CONCAT:
log.path data: /article/candidate-is-jerk 
articles.slug data: candidate-is-jerk 

CONCAT adds "/article/" to the beginning of every piece of slug data thus allowing me to join the log and articles tables together.

6. Then I grouped it by the name of the articles and ordered them by which article had the most connections
aka "views" on the log table. 
7. I then printed a name for the list that will be returned and then indented the results using \t, then the title article, then a hyphen to separate the article name from it's number of views.
In summary: the functions returns the title of the article as well as a count of all the times that the slug=path
aka everytime the article was viewed.

# Explanation of code for most_pop_authors():
Selects the author name and the title of each article every time the
slug+path between the articles table and the log table match up as well as when the authors match up with their own articles (articles.author=authors.id) thus creating a count of the number of times each authors' work was viewed cumulatively. 

In summary: this function determines the number of time each article was viewed and then it matches up the articles with the name of the author for who it belongs. In the end, it creates a total count of how many times a particular author's work was viewed. 

This is almost identical to the "most popular articles" function above except that I added the "AND articles.author=authors.id"

# Explanation of code for error_dates():
For this function I needed to create two views. They are as follows:

>CREATE VIEW all_connections AS SELECT substring(time::text, 0, 11)
>AS DATE, COUNT(status) AS all FROM log GROUP BY date ORDER BY date DESC;

all_connections: a view that lists all the dates in order by date
along with the number of views on each day (all = number of connections)

The second view I created is as follows:

>CREATE VIEW not_running AS SELECT substring(time::text, 0, 11) AS DATE,
>COUNT(status) AS not_ok FROM log WHERE status='404 NOT FOUND' GROUP BY
>date ORDER BY date DESC;

This view displays the number of times the connections failed
aka where there was a "404 not found" error.
This view was also ordered by date allowing me to connect all_connections with not_running since both have a matching column (date) 
Using both views I combined their data into one table.

The query in the function above converts the date within each table
from YYYY-MM-DD to Month Day, Year
it then selects both the number of errors from the "not_running" view
as well as the total number of connections from the "all_connections" view
and and divides them. From there, the WHERE command determines
which dates/ decimals will be displayed since it will only display
dates where the error percentage is greater than 1.0.
Within the python code, I added a "%" to the end of the decimal so the
user sees it as a percentage. The ROUND function is used so that the
decimal produced only has two decimal places. 
