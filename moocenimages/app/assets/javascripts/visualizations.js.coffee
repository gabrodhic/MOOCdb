# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$ ->
  $("div.pipeline a").click (ev) =>
    target = $(ev.target)

    $("div.pipeline li").removeClass('active')
    target.closest('li').addClass('active')
    
    vizstep = target.closest('a').data('vizstep')
    content = ""

    if vizstep == 1
      content = 'MOOCDB: the universal database schema for MOOC data.'
    else if vizstep == 3
      content = 'Private data file: we do not host the private data file contents.'
    else if vizstep == 7
      content = 'Visualization: viewable by scrolling up.'
    else
      ajaxData = 
        offering_id: parseInt($('.offering :selected').val())
        visualization_id: $('.viz-name').data('vizid')
        visualization_step_id: vizstep
      $.ajax '/get_upload',
        type: 'POST'
        contentType: 'application/json'
        data: JSON.stringify(ajaxData)
          


      content = ''

    $('#code-block').html(content)
    return false