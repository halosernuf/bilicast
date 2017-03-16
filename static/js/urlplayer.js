var player;
var currentUrl = '';

$(function() {
  player = new CastPlayer();
});

function getUrlParameter(sParam) {
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split('&');
  for (var i = 0; i < sURLVariables.length; i++)  {
    var sParameterName = sURLVariables[i].split('=');
    if (sParameterName[0] == sParam) {
      return decodeURIComponent(sParameterName[1]);
    }
  }
}

function launchApp() {
  player.launchApp();
}

function startPlayback(url,name,img) {
  
  if (player.session == null) {
    player.launchApp();
    return;
  }
  contentType="video/mp4";
  player.loadMedia(url, contentType, name, img);
  $('#player_now_playing').html(name);
}

function pause() {
  if (player.session != null) {
    player.pauseMedia();
  }
}

function resume() {
  if (player.session != null) {
    player.playMedia();
  }
}

function seek(is_forward) {
  if (player.session != null) {
    player.seekMedia(is_forward);
  }
}

function seekTo() {	
  if (player.session != null) {
    player.seekTo(parseInt($("#player_seek_range").val()));
  }
}

function stop() {
    $("#control-panel").hide();
    $("#launch-button").show();
    player.stopApp();
}

function volumeDown() {
  if (player.session != null) {
      player.volumeControl(false, false);
  }
}

function volumeUp() {
  if (player.session != null) {
    player.volumeControl(true, false);
  }
}

function volumeMute() {
  if (player.session != null) {
    player.volumeControl(false, true);
  }
}