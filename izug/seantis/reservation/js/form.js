(function($){
    $(document).ready(function() {
        /*
        the kita fields behavior kinda supplements the facility fields,
        and this is not nice for the user. I would love to do this right, but
        I need this kinda fast.
        */
        if ($('#formfield-form-widgets-IKitaZugFields-affix').length > 0) {
            $('#formfield-form-widgets-contact').hide();
            $('#formfield-form-widgets-infrastructure').hide();
            $('#formfield-form-widgets-terms_of_use').hide();
            $('#formfield-form-widgets-description').hide();
        }
    });
})(jQuery);