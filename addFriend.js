$(function(){
	$('button').click(function(){
		var friend = $('#friend').val();
		var friendGroup = $('#friendGroup').val();
		$.ajax({
			url: '/addFriendGroup',
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