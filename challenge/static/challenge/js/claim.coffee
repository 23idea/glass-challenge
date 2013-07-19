$(document).ready (e)->
  url = 'http://www.youtube.com/embed/'

  for link in $(".proof")
    href = link.href
    yt_id = href.trim().match(/v=(\w+)/)[1]
    iframe = document.createElement('iframe')
    iframe.src = url + yt_id
    $(link).parent().parent().append(iframe)
