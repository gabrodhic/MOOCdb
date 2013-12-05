# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$ ->
  get_upload_ajax = (ajaxData) =>
    $.ajax '/get_upload',
      type: 'POST'
      contentType: 'application/json'
      dataType: 'json'
      data: JSON.stringify(ajaxData)
      success: (data) =>
        $('.file-name').html(data['file_name'])
        $('#code-block code').html(data['contents'])
        $('.download-file').show()
        $('.download-file').attr('href', data['download_url'])
      error: =>
        $('.file-name').html('Error')
        $('#code-block code').html('There was an error in fetching this file.')
        $('.download-file').hide()
  
  initialize_page = () =>
    ajaxData = 
      offering_id: parseInt($('.offering :selected').val())
      visualization_id: $('.viz-name').data('vizid')
      visualization_step_id: 2

    get_upload_ajax(ajaxData)

  initialize_page()

  $("div.pipeline a").click (ev) =>
    target = $(ev.target)

    $("div.pipeline li").removeClass('active')
    target.closest('li').addClass('active')
    
    vizstep = target.closest('a').data('vizstep')
    content = ""

    if vizstep == 1
      filename = 'MOOCDB'
      content = 'MOOCDB: the universal database schema for MOOC data.'
    else if vizstep == 3
      filename = 'Private Data'
      content = 'Private data file: we do not host the private data file contents.'
    else if vizstep == 7
      filename = 'Visualization'
      content = 'Visualization: viewable by scrolling up.'
    else
      ajaxData = 
        offering_id: parseInt($('.offering :selected').val())
        visualization_id: $('.viz-name').data('vizid')
        visualization_step_id: vizstep

      get_upload_ajax(ajaxData)
      return false

    $('.file-name').html(filename)
    $('#code-block code').html(content)
    $('.download-file').hide()
    return false

  $("select.offering").change (ev) =>
    initialize_page()
