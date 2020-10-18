$(function(){
	$('button').click(function(){
		var pokeEmail = $('#toBePoked').val();
		$.ajax({
			url: '/poke',
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