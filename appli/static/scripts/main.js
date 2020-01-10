var u_name = $('#u_id').data('name')
var u_id = $('#u_id').data('id')
var send_mess = document.getElementById("send_mess")
var message = document.getElementById("message_txt")

$(document).ready(function(){
  	$('.toast').toast('show')
})

send_mess.onclick = function(){
	event.preventDefault()
	var txt = $('#message_txt').val()
	console.log(u_name+" a écrit:"+message.value)
	$.post('/',
		{'user_id': u_id,
		 'message': txt
		},
		function(result){
		document.location.reload(true)
		var res = JSON.parse(results)
		})	
}
