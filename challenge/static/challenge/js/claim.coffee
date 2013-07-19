$(document).ready (e)->
  url = 'http://www.youtube.com/embed/'

  for link in $(".proof")
    href = link.href
    yt_id = href.trim().match(/v=(\w+)/)[1]
    iframe = document.createElement('iframe')
    iframe.src = url + yt_id
    iframe.height = 236
    iframe.width = 420
    $(link).parent().parent().append(iframe)

  if QueryString.thanks
    $("#modalThanks").modal()
