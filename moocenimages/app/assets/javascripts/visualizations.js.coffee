# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$ ->
  $(".datepicker").datepicker()

  window.path_to_public_data = $("#visualization-jumbotron").data('url')
  $('#visualization-frame').attr('src', $('#visualization-frame').data('url'))

  get_upload_ajax = (ajaxData) =>
    $.ajax '/get_upload',
      type: 'POST'
      contentType: 'application/json'
      dataType: 'json'
      data: JSON.stringify(ajaxData)
      success: (data) =>
        $('.file-name').html(data['file_name'])
        $('#code-block code').html(data['contents'].replace(/>/gi, '&gt').replace(/</gi, '&lt'))
        $('.download-file').show()
        $('.download-file').attr('href', data['download_url'])
      error: =>
        $('.file-name').html('Error')
        $('#code-block code').html('There was an error in fetching this file.')
        $('.download-file').hide()

  get_path_to_public_data_ajax = () =>
    ajax_data =
      offering_id: parseInt($('.offering :selected').val())
    $.ajax '/get_path_to_public_data',
      type: 'POST'
      contentType: 'application/json'
      dataType: 'json'
      data: JSON.stringify(ajax_data)
      success: (data) =>
        window.path_to_public_data = data['path_to_public_data']
        $('#visualization-frame').attr('src', $('#visualization-frame').attr('src'))

  initialize_page = () =>
    offeringID = parseInt($('.offering :selected').val())
    vizID = $('.viz-name').data('vizid')

    if offeringID? && vizID?
      ajaxData =
        offering_id: offeringID
        visualization_id: vizID
        visualization_step_id: 2

      get_upload_ajax(ajaxData)

      $('.download-zip').attr('href', '/get_zip?visualization_id=' + vizID.toString() + '&offering_id=' + offeringID.toString())

  current_url = document.URL
  if current_url.indexOf('new') == -1
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
        filename = 'Exported Data'
        content = 'Exported Data file: we do not host the Exported Data file contents.'
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
      get_path_to_public_data_ajax()
  else
    $('input:file').change =>
      $('button:submit').removeAttr('disabled')
