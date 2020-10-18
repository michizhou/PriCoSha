$(function(){
	$('button').click(function(){
		var user = $('#username').val();
		var pass = $('#password').val();
		$.ajax({
			url: '/authenticateUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				alert("Username or Password does not exist")
				console.log(error);
			}
		});
	});
});