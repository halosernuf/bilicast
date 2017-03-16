var metadata;

$(function() {
  $('#btn').click(function() {
    $.getJSON($SCRIPT_ROOT + '/getData', {
      url: $('input[name="url"]').val(),
    }, function(data) {
        // console.log(data)
        var table=$('#res tbody');
        var html="";
        for(i=0;i<data.length;i++){
          // console.log(data[i]['title'])
          var name=data[i]['title']+" "+data[i]['pagename']
          html+=("<tr><td>"+
            "<button class='btn btn-default cast' value='"+data[i]['cid']+
            "' name='"+name+
            "' type='button'>Cast!</button>"+
            "</td><td>"+name+
            "</td><td>"+data[i]['cid']+
            "</td></tr>");
        }
        table.html(html);
        $('.cast').click(function() {
          var cid=$(this).context.value;
          var name=$(this).context.name;
          var img=data[0]['img'];
          $.getJSON($SCRIPT_ROOT + '/getUrl', {
            cid: cid
          },function(data){
            var regex=/rate=(.*)/g;
            var match=regex.exec(data[0]);
            if(match!=null){console.log('rate='+match[1]);}
            startPlayback(data[0],name,img);
          });
        });
      });
    return false;
  });
});