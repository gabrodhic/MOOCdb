# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$ ->
  file_contents = {}
  file_contents[1] = 'MOOCDB: the universal database schema for MOOC data.'
  file_contents[3] = 'Private data file: we do not host the private data file contents.'
  file_contents[7] = 'Visualization: viewable by scrolling up.'
  
  $("div.pipeline a").click (ev) =>
    target = $(ev.target)

    $("div.pipeline li").removeClass('active')
    target.closest('li').addClass('active')
    
    vizstep = target.closest('a').data('vizstep')
    content = file_contents[parseInt(vizstep)]

    $('#code-block').html(content).fadeIn('fast')
    return false