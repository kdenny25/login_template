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
