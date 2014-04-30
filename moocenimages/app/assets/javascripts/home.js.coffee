# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$ ->
  contents1 = "#visualization_script.html\n\n...\n&lt;script type='javascript'&gt;\n...  \n  d3.csv('public_data.csv', function(error, data) {\n    ...\n  }\n  ...\n&lt;/script&gt;"
  $('.public_data_instructions code1').html(contents1)

  contents2 = "#visualization_script.html\n\n...\n&lt;script type='javascript'&gt;\n...  \n  d3.csv(window.parent.path_to_public_data, function(error, data) {\n    ...\n  }\n  ...\n&lt;/script&gt;"
  $('.public_data_instructions code2').html(contents2)

  contents3 = "#visualization_container.html\n\n&lt;html&gt;\n  &ltbody&gt;\n    &lt;script type='javascript'&gt;\n      var window.parent.path_to_public_data = 'public_data.csv';\n    &lt;/script&gt;\n\n    &lt;iframe src='visualization_script.html' height='500' id='visualization-frame' scrolling='no' width='1000'&gt;&lt;/iframe&gt;\n\n  &lt;/body&gt;\n&lt;/html&gt;"
  $('.public_data_instructions code3').html(contents3)