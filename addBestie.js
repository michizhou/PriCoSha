$(function(){
	$('button').click(function(){
		var bestieEmail = $('#bestieEmail').val();
		$.ajax({
			url: '/addBestFriend',
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