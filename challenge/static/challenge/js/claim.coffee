$(document).ready (e)->
  url = 'http://www.youtube.com/embed/'
  href = $("#proof")[0].href
  yt_id = href.trim().match(/v=(\w+)/)[1]
  iframe = document.createElement('iframe')
  iframe.src = url + yt_id
  $("#claim_content").append(iframe)
