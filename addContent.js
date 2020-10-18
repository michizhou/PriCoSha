$(function(){
	$('button').click(function(){
		var postTitle = $('#title').val();
		var postBody = $('#body').val();
		var isPublic = $('#public').val();
		$.ajax({
			url: '/addContent',
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