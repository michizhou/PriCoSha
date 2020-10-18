$(function(){
	$('button').click(function(){
		var friendGroup = $('#friendGroup').val();
		var friendGroupDes = $('#friendGroupDes').val();
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