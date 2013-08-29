'''

Created on Jun 24, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb 


#!/usr/bin/python
# -*- coding: utf-8 -*-

def generate_html(options):
    '''
    
    '''
    
    print "ok"
    if options.get_chart_type() == "area_chart":
        print options.get_chart_type()
        html = generate_area_chart(options)
    
    if options.get_chart_type() == "column_chart":
        print options.get_chart_type()
        html = generate_column_chart(options)
        
    if options.get_chart_type() == "geo_map":
        print options.get_chart_type()
        html = generate_geo_map(options)
        
    if options.get_chart_type() == "line_chart":
        print options.get_chart_type()
        html = generate_line_chart(options)
        
    if options.get_chart_type() == "pie_chart":
        print options.get_chart_type()
        html = generate_pie_chart(options)
           
        
    
        
    
    
    file_output = open(options.get_output_file(), 'w')
    file_output.write(html)
    file_output.close()
    

def generate_pie_chart(options):
    
    html = '''
    <html>
    <head>
      <script type="text/javascript" src="https://www.google.com/jsapi"></script>
      <script type="text/javascript">
       google.load("visualization", "1", {packages:["corechart"]});
       google.setOnLoadCallback(drawChart);
       function drawChart() {
        var data = google.visualization.arrayToDataTable([
    '''
    
    html += options.get_data()
    #print options.get_chart_title(), options.get_page_title(), str(options.get_width()), str(options.get_height())
    html += '''
        ]);
        
        var options = {
         title: '%s'
        };
    
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
       }
      </script>
     </head>
     <body>
      %s
      <div id="chart_div" style="width: %spx; height: %spx;"></div>
     </body>
    </html>
    ''' % (options.get_chart_title(), options.get_page_title(), str(options.get_width()), str(options.get_height()))
    
    return html



def generate_area_chart(options):
    '''
    
    '''
    html = '''
    <html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
        '''
    
    html += options.get_data()
    
    html += '''
        ]);
    
            var options = {
              title: '%s',
              hAxis: %s,
              vAxis: %s
            };
    
            var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>    
          %s
          <div id="chart_div" style="width: %spx; height: %spx;"></div>
      </body>
    </html>
    ''' % (options.get_chart_title(), options.get_h_axis(), options.get_v_axis(), options.get_page_title(), str(options.get_width()), str(options.get_height()))

    return html


def generate_column_chart(options):
    '''
    
    '''
    html = '''
    <html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
        '''
    
    html += options.get_data()
    
    html += '''
        ]);
    
            var options = {
              title: '%s',
              hAxis: %s,
              vAxis: %s
            };
    
            var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>    
          %s
          <div id="chart_div" style="width: %spx; height: %spx;"></div>
      </body>
    </html>
    ''' % (options.get_chart_title(), options.get_h_axis(), options.get_v_axis(), options.get_page_title(), str(options.get_width()), str(options.get_height()))

    return html


def generate_line_chart(options):
    '''
    
    '''
    html = '''
    <html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
        '''
    
    html += options.get_data()
    
    html += '''
        ]);
    
            var options = {
              title: '%s',
              hAxis: %s,
              vAxis: %s
            };
    
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>    
          %s
          <div id="chart_div" style="width: %spx; height: %spx;"></div>
      </body>
    </html>
    ''' % (options.get_chart_title(), options.get_h_axis(), options.get_v_axis(), options.get_page_title(), str(options.get_width()), str(options.get_height()))

    return html
    
 
def generate_geo_map(options):
    '''
    
    '''
    html = '''
    <html>
    <head>
      <script type='text/javascript' src='https://www.google.com/jsapi'></script>
      <script type='text/javascript'>
       google.load('visualization', '1', {'packages': ['geomap']});
       google.setOnLoadCallback(drawMap);
    
        function drawMap() {
          var data = google.visualization.arrayToDataTable([
        '''
    
    html += options.get_data()
    
    html += '''
    ]);

      var options = {};
      options['dataMode'] = 'regions';
      options['width'] = %s;
      options['height'] = %s;
      options['showLegend'] = true;
      options['colors']=[0xffffaa, 0xCC3300]; // yellow to red
      
        var container = document.getElementById('map_canvas');
      var geomap = new google.visualization.GeoMap(container);
      geomap.draw(data, options);
  };
  </script>
    </head>
    
    <body>
    %s<br/> <br/>
      <div id='map_canvas'></div>
    </body>
    
    </html>
    '''  % (str(options.get_width()), str(options.get_height()), options.get_page_title())

    return html   


def run_query(sql):
    '''
    
    '''
    connection = mdb.connect('127.0.0.1', 'root', 'database_password', 'moocdb') #, charset='utf8', use_unicode=True);    
    cursor = connection.cursor()
    cursor.execute(sql)    
    connection.commit()
    connection.close()   
    
        
def get_data(sql):
    '''
    
    '''
    connection = mdb.connect('127.0.0.1', 'root', 'database_password', 'moocdb') #, charset='utf8', use_unicode=True);
    
    cursor = connection.cursor()
    cursor.execute(sql)
    
    # http://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
    
    print field_names
    graph_data = str(field_names)
    
    if cursor.rowcount < 1:
        print "The query returned no results" 
        return
    
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        #print list(row)
        graph_data +=  ","
        graph_data += str(list(row))
        graph_data = graph_data.replace("L]", "]")
        graph_data = graph_data.replace("L,", ",")
        
        # Remove e.g. [0, Decimal('121.4130')]
        graph_data = graph_data.replace(", Decimal('", ", ")
        graph_data = graph_data.replace("[Decimal('", "[")
        graph_data = graph_data.replace("')]", "]")
        graph_data = graph_data.replace("'),", ",")
        
    
    connection.close()   
    
    return graph_data

class options():
        
    def __init__(self):
        pass
        '''
        self.data = data
        self.chart_type = chart_type
        self.title = title
        '''

    def get_h_axis(self):
        return self.__h_axis


    def get_v_axis(self):
        return self.__v_axis


    def set_h_axis(self, value):
        self.__h_axis = value


    def set_v_axis(self, value):
        self.__v_axis = value


    def del_h_axis(self):
        del self.__h_axis


    def del_v_axis(self):
        del self.__v_axis


    def get_output_file(self):
        return self.__output_file


    def set_output_file(self, value):
        self.__output_file = value


    def del_output_file(self):
        del self.__output_file


    def get_data(self):
        return self.__data


    def get_chart_type(self):
        return self.__chart_type


    def get_title(self):
        return self.__title


    def get_page_title(self):
        return self.__page_title


    def get_chart_title(self):
        return self.__chart_title


    def get_width(self):
        return self.__width


    def get_height(self):
        return self.__height


    def set_data(self, value):
        self.__data = value


    def set_chart_type(self, value):
        self.__chart_type = value


    def set_title(self, value):
        self.__title = value


    def set_page_title(self, value):
        self.__page_title = value


    def set_chart_title(self, value):
        self.__chart_title = value


    def set_width(self, value):
        self.__width = value


    def set_height(self, value):
        self.__height = value


    def del_data(self):
        del self.__data


    def del_chart_type(self):
        del self.__chart_type


    def del_title(self):
        del self.__title


    def del_page_title(self):
        del self.__page_title


    def del_chart_title(self):
        del self.__chart_title


    def del_width(self):
        del self.__width


    def del_height(self):
        del self.__height

            
    #data = ""
    #chart_type = ""
    #title = ""
    data = ""
    chart_type =  ""
    title = ""
    page_title = ""
    chart_title = ""
    width = 0
    height = 0
    output_file = ""
    h_axis = ""
    v_axis = "" 
    
    data = property(get_data, set_data, del_data, "data's docstring")
    chart_type = property(get_chart_type, set_chart_type, del_chart_type, "chart_type's docstring")
    title = property(get_title, set_title, del_title, "title's docstring")
    page_title = property(get_page_title, set_page_title, del_page_title, "page_title's docstring")
    chart_title = property(get_chart_title, set_chart_title, del_chart_title, "chart_title's docstring")
    width = property(get_width, set_width, del_width, "width's docstring")
    height = property(get_height, set_height, del_height, "height's docstring")
    output_file = property(get_output_file, set_output_file, del_output_file, "output_file's docstring")
    h_axis = property(get_h_axis, set_h_axis, del_h_axis, "h_axis's docstring")
    v_axis = property(get_v_axis, set_v_axis, del_v_axis, "v_axis's docstring")
    

