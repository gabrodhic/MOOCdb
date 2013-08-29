

#list.of.packages <- c("RMySQL")
#new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
#if(length(new.packages)) install.packages(new.packages)


#Sys.getenv("MYSQL_HOME")
#install.packages('RMySQL',type='source') 


# Install  http://cran.r-project.org/web/packages/RMySQL/index.html
# For Windows 7: http://stackoverflow.com/questions/5223113/using-mysql-in-r-for-windows
library(RMySQL) # will load DBI as well

# Open a connection to a MySQL database
connection <- dbConnect(MySQL(), user="root", password="database_password", dbname="moocdb", host="localhost") 

## list the tables in the database
dbListTables(connection)

# Print all first 1000 users
rs = dbSendQuery(connection, "SELECT * FROM users LIMIT 1000")
data = fetch(rs, n=-1)
data

# More documentation: http://rss.acs.unt.edu/Rdoc/library/RMySQL/html/RMySQL-package.html

# Close connections:
dbDisconnect(connection)