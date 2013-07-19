$(document).ready (e)->
  $(".login").on "click", (e)->
    $("#modalLogin").modal()

  #voting mechinism
  $(".vote").on "click", (e)->
    id = $(this).data("id")
    dir = $(this).data("dir")
    val = $("#challenge_"+id).text()

    if $(this).hasClass("voted")
      $("[data-id="+id+"]").removeClass("voted")
      if dir == "up"
        val = Number(val) - 1
      else if dir == "down"
        val = Number(val) + 1

      dir = ""
    else
      if $("[data-id="+id+"]").hasClass("voted")
        if dir == "up"
          val = Number(val) + 1
        else if dir == "down"
          val = Number(val) - 1

      $("[data-id="+id+"]").removeClass("voted")
      $(this).addClass("voted")
      if dir == "up"
        val = Number(val) + 1
      else if dir == "down"
        val = Number(val) - 1

    $("#challenge_"+id).text(val)
    $.get("vote", {challenge:id ,dir:dir })

  #url pasring
  url = 'https://img.youtube.com/vi/'
  for link in $(".yt_link")
      href = link.textContent
      if href isnt "False"
        yt_id = href.trim().match(/v=(\w+)/)[1]
        newImg = document.createElement('img')
        newImg.src = url + yt_id + "/default.jpg"
        newImg.className = "proof_thumb"
        $(link).parent().prepend(newImg)
