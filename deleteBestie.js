$(function(){
	$('button').click(function(){
		var bestieEmail = $('#bestieEmail').val();
		$.ajax({
			url: '/deleteBestFriend',
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