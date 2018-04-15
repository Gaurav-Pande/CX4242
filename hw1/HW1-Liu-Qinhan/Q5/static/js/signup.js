$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});

		var para = document.createElement("p");
		para.setAttribute("style", "text-align=center");
		var mess = document.createTextNode("Congratulations on registering for CSE6242, "+ user + "! Redirecting you to the course homepage...")
		para.appendChild(mess);
		var element = document.getElementById("div1");
		element.appendChild(para);

		this.form.elements["username"].value = '';
		this.form.elements["password"].value = '';

		setTimeout( function(){ window.location.replace("http://poloclub.gatech.edu/cse6242/2018spring/"); }, 3000);
	});
});