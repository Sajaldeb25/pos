function checkFieldError() {
    if ($('#name_error').length) {
        var nameError = JSON.parse($('#name_error').text());
        $('#name_error_text').text(nameError);
        $('#id_name').addClass('error_border');

    } else {
        nameError = '';
        $('#id_name').removeClass('error_border');
    }

    if ($('#mobile_no_error').length) {
        var mobileError = JSON.parse($('#mobile_no_error').text());
        $('#mobile_no_error_text').text(mobileError);
        $('#id_mobile_no').addClass('error_border');
    } else {
        mobileError = '';
        $('#mobileError').removeClass('error_border');
    }

    if ($('#address_error').length) {
        var addressError = JSON.parse($('#address_error').text());
        $('#address_error_text').text(addressError);
        $('#id_address').addClass('error_border');
    } else {
        addressError = '';
        $('#id_address').removeClass('error_border');

    }

    if ($('#customer_phone_error').length) {
        var customerPhoneError = JSON.parse($('#customer_phone_error').text());
        $('#customer_phone_error_text').text(customerPhoneError);
        $('#new_customer_phone').addClass('error_border');
    } else {
        customerPhoneError = '';
        $('#new_customer_phone').removeClass('error_border');

    }
}
