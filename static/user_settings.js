$(function(){
    $('#new_profile_pic').on('change', function(){
        console.log($('#new_profile_pic').prop('files'))
        var pic = $('#new_profile_pic').get(0).files[0];

        if(pic){
            var reader = new FileReader();
            reader.onload = function(){
                $('#profile_pic_preview').attr("src", reader.result);

            }
            reader.readAsDataURL(pic)
        }
    })
})

$('#theme-select').on('change', function(){
    var theme = $(this).find(":selected").val();

    $.ajax({
        type: 'POST',
        url: '/save_theme',
        data: {
            theme : theme
        },
        success: function(data){
            console.log('Success')
            $('#theme-saved').fadeIn(500).fadeOut(5000)
        }
    })
})

function validateEmail($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test( $email )
}

$('#update-user-info').on('click', function() {
    var user_name = $('#name').val()
    var user_email = $('#email').val()
    var email_error = $('#email-error')

    email_error.hide()

    if(validateEmail(user_email)){
        // ********************
        // Send validation email
        // in some function here
        // ********************
        $.ajax({
            type: 'POST',
            url: '/save_info',
            data: {
                name: user_name,
                email: user_email
            },
            success: function(data){
                console.log(data.data)
            }
        })
    } else {
        email_error.show()
    }
})

$('#submit-pw-change').on('click', function() {
    var pw = $('#old-pw').val()
    var new_pw = $('#new-pw').val()
    var new_pw_confirm = $('#new-pw-confirm').val()

    var old_pw_error = $('#old-pw-error')
    var new_pw_error = $('#new-pw-confirm-error')

    old_pw_error.hide()
    new_pw_error.hide()

    // Check if old password matches
    $.ajax({
        type: 'POST',
        url: '/validate_pw',
        data: {
            old_password: pw
        },
        success: function(data){
            var result = data.result
            console.log(result)
            if(result === false){
                old_pw_error.show()
                pw = ''
                new_pw = ''
                new_pw_confirm = ''
            } else {
                if(new_pw !== new_pw_confirm){
                    new_pw_error.show()
                    pw = ''
                    new_pw = ''
                    new_pw_confirm = ''
                } else {
                    $.ajax({
                        type: 'POST',
                        url: '/update_pw',
                        data: {
                            new_password: new_pw_confirm
                        },
                        success: function(){
                            $('#pw-updated').fadeIn(500).fadeOut(2000)
                        }
                    })
                }
            }
        }
    })
})
