$(function() {
    var form_id = '#id_profile_form';
    var options = { 
        target: form_id,
        beforeSubmit: function(){
            $('input, select, textarea').attr("disabled", "true");
            $('#id_ajax_loader').css('display', 'inline');
            $('#id_message_holder').text('');
        },
        success: function(){
            $('input, select, textarea').removeAttr("disabled");
            $('#id_ajax_loader').css('display', 'none');
            if ($.find("ul.errorlist").length==0){
                $('#id_message_holder').text('Changes have been saved.');
            }
        }
    };
    $(form_id).ajaxForm(options);
});

