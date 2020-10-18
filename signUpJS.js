$(function(){
	$('button').click(function(){
		var user = $('#new_username').val();
		var pass = $('#new_password').val();
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});