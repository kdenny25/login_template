function register(){
    var csrf_token = "{{ csrf_token() }}"
    var name = $('#reg-name').val()
    var email = $('#reg-email').val()
    var password = $('#reg-password').val()
    var confirm_password = $('#reg-confirm-password').val()

    email_url = "/email_exists?email=" + email
    fetch(email_url, {
        method: "GET"
    }).then(response =>{
        return response.text();
    }).then(result => {
        var result = jQuery.parseJSON(result)
        console.log(result.result)
        if(result.result === true){
            $('#reg-email-error').text('Email already exists')
        } else {
            $('#reg-email-error').text('')
            if(password !== confirm_password){
                $('#reg-password-error').text("Passwords don't match")
            } else {
                $('#reg-password-error').text('')
                $.ajax({
                    type: 'POST',
                    url: '/register_user',
                    headers: {
                        "X-CSRFToken": csrf_token,
                    },
                    data: {
                        name : name,
                        email : email,
                        password : password
                    },
                    success: function(data) {
                        console.log(data.result)
                    }
                });
            }
        }

    })



}

$(".show-pw").on("click", function(){
    var pw_input = $(this).parent().find('.password')
    console.log($(this).parent().find('.password').attr('type'))
    $(this).find('path').toggle()

    if(pw_input.attr("type") === "password"){
        pw_input.attr("type", "text")
    } else {
        pw_input.attr("type", "password")
    }
})