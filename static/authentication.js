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
        console.log(result)
    })
    // $.ajax({
    //     type: 'POST',
    //     url: '/email_exists',
    //     headers: {
    //         "X-CSRFToken": csrf_token,
    //     },
    //     data: {
    //         email : email
    //     },
    //     success: function(data) {
    //         console.log(data.result)
    //     }
    // });

    if(password !== confirm_password){
        console.log("Passwords don't match")
    }
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