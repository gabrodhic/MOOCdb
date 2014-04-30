# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$ ->
  contents1 = "#visualization_script.html\n\n...\n&lt;script type='javascript'&gt;\n  ...\n  d3.csv('public_data.csv', function(error, data) {\n    ...\n  }\n  ...\n&lt;/script&gt;\n..."
  $('.public_data_instructions code1').html(contents1)

  contents2 = "#visualization_script.html\n\n...\n&lt;script type='javascript'&gt;\n  ...\n  d3.csv(window.parent.path_to_public_data, function(error, data) {\n    ...\n  }\n  ...\n&lt;/script&gt;\n..."
  $('.public_data_instructions code2').html(contents2)