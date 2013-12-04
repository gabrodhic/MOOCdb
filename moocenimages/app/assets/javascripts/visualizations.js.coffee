# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$(document).ready ->
  $("div.pipeline a").click (ev) =>
    $("div.pipeline li").removeClass('active')
    $(ev.target).closest('li').addClass('active')
    return false