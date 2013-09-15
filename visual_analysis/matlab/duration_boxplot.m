% Created on Jun 25, 2013
% @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

%% connection to MySQL server
% Nice tuto: http://www.stanford.edu/group/farmshare/cgi-bin/wiki/index.php/MatlabMysql

% Database Server
%host = 'mysql-user.stanford.edu';
host = '127.0.0.1:3306';

% Database Username/Password
user = 'root';
password = 'database_password';

% Database Name
dbName = 'moocdb';

% JDBC Parameters
jdbcString = sprintf('jdbc:mysql://%s/%s', host, dbName);
jdbcDriver = 'com.mysql.jdbc.Driver';

% Set this to the path to your MySQL Connector/J JAR
% Download it here: http://dev.mysql.com/downloads/connector/j/
% javaaddpath('/usr/share/java/mysql-connector-java.jar')
javaaddpath('C:\server\mysql-connector-java-5.1.25\mysql-connector-java-5.1.25-bin.jar')

% Create the database connection object
connection = database(dbName, user , password, jdbcDriver, jdbcString)

% Check to make sure that we successfully connected
if isconnection(connection)
	% Fetch the symbol, market cap, and last close for the 10 largest
	% market cap ETFs
	%result = get(fetch(exec(connection, 'SELECT user_id FROM moocdb.users LIMIT 1000')), 'Data');
	%disp(result);
else
	% If the connection failed, print the error message
	disp(sprintf('Connection failed:&nbsp;%s', connection.Message));
end


%% Running queries
% http://www.mathworks.com/help/database/run-sql-query.html

sql = [' SELECT observed_events.observed_event_duration ' ... 
    ' FROM moocdb.observed_events AS observed_events ' ...
    ' WHERE observed_events.observed_event_duration < 200' ...
    ' LIMIT 100000; '];

cursor = exec(connection,sql);
a = fetch(cursor);
data = cell2mat(a.Data);

boxplot(data)
title('Distribution of the duration of observed events')
ylabel('Duration (in seconds)')
print('-dpng','-r300', ['observed_events_duration_boxplot'])
saveas(figure(1), 'observed_events_duration_boxplot', 'fig')

plot(sort(data))
title('Distribution of the duration of observed events')
ylabel('Duration (in seconds)')
print('-dpng','-r300', ['observed_events_duration_plot'])
saveas(figure(1), 'observed_events_duration_plot', 'fig')


% LIMIT 1000000 because more rows blows MATLAB...

% Close the connection so we don't run out of MySQL threads
close(connection);