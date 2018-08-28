# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2

DBNAME = "news"

# What are the most popular three articles of all time?


def most_pop_article():
    db = psycopg2.connect(dbname=DBNAME, port=5432)  # connects to database
    c = db.cursor()
    c.execute(""" SELECT title, COUNT(title) AS views
      FROM articles, log WHERE CONCAT('/article/', slug)=path
      GROUP BY title ORDER BY views DESC LIMIT 3;""")
    pop_articles = c.fetchall()
    print("Most Popular Articles by Views:")
    for result in pop_articles:
        print("\t", result[0], "-", str(result[1]), "Views")
    # print(pop_articles)
    db.close()

most_pop_article()

# explanation of code above:
# using psycopg2 we can connect to the databse using DNname
# db.cursor() allows python to exectue a postgreSQL command
# Using c.execute, it calls the function 'cursor' and executes
# the sql command
# within this function I created a SQL query that will display the
# name of the articles along with the number of views each had
# I did this by joining the "articles" and "log" tables and using
# CONCAT to make sure that "path" in log and "slug" in articles
# matched. then I grouped it by the name of the articles
# and ordered them by which article had the most connections
# aka "views" on the log table
# I then printed a name for the list that will be returned
# and then indented the results using \t, then the title article,
# then a hyphen to separate the article name from it's number of
# views
# returns the title of the article as well as a count
# of all the times that the slug=path
# aka everytime the article was viewed

# 2. Who are the most popular article authors of all time? That is, when you
# sum up all of the articles each author has written, which authors get
# the most page views? Present this as a sorted list with the most popular
# author at the top.


def most_pop_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT authors.name, COUNT(articles.title)
              AS views FROM authors, log, articles
              WHERE  CONCAT('/article/', slug)=path
              AND articles.author=authors.id
              GROUP BY authors.name ORDER BY views DESC;""")
    most_pop_authors = c.fetchall()
    print("Author Popularity by Views:")
    for result in most_pop_authors:
        print ("\t", result[0], "-", str(result[1]), "Views")
    db.close()

most_pop_authors()

# explanation for code above!:
# selects the author name and the title of each article every time the
# slug+path match up as well as when the authors match up with
# their own articles thus creating a
# count of the number of times it was viewed cumulativelY
# this is almost idential to the "most popular articles" function above
# except that I added the "AND articles.author=authors.id"


# 3. On which days did more than 1% of requests lead to errors?
# The log table includes a column status that indicates the HTTP status code
# that the news site sent to the user's browser. (Refer to this lesson for
# more information about the idea of HTTP status codes.)
# Example:
# July 29, 2016 — 2.5% errors


def error_dates():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(""" SELECT
                  TO_CHAR(not_running.date::timestamp, 'Month DD, YYYY'),
                  ROUND(100.0*not_running.not_ok/all_connections.all, 2)
                  AS error_pct
                  FROM not_running, all_connections
                  WHERE all_connections.date=not_running.date
                  AND 100.0*not_running.not_ok/all_connections.all>1.0;""")
    error_dates = c.fetchall()
    print("Error Percentage by Date:")
    for result in error_dates:
        print ("\t", result[0], "-", str(result[1]) + "%", "Errors")
    return error_dates

error_dates()

#
# for this function I needed to create two views. They are as follows:
# CREATE VIEW all_connections AS SELECT substring(time::text, 0, 11)
# AS DATE, COUNT(status) AS all FROM log GROUP BY date ORDER BY date DESC;
# all connections: a view that lists all the dates in order by date
# along with the number of views on each day (all = number of connections)
# I used the substring function to only
# incorporate the date (YYYY-MM-DD) into the table

# The second view I created is as follows:

# CREATE VIEW not_running AS SELECT substring(time::text, 0, 11) AS DATE,
# COUNT(status) AS not_ok FROM log WHERE status='404 NOT FOUND' GROUP BY
# date ORDER BY date DESC;
# This view displays the number of times the connections failed
# aka where there was a "404 not found" error.
# This view was also ordered by date allowing me to connect them in the SQL
# query that I used in the function
# Using both views I combined their data into one table
# The query in the function above first converts the date within each table
# from YYYY-MM-DD to Month Day, Year
# it then selects both the number of errors from the "not_running" view
# as well as the total number of connections from the "all_connections" view
# and and divides them together. From there, the WHERE command determines
# which dates/ decimals will be displayed since it will only display
# dates where the error percentage is greater than 1%
# within the python code, I added a "%" to the end of the decimal so the
# user sees is as a percentage. The ROUND function is used so that the
# decimal produced only has two decimal places.
