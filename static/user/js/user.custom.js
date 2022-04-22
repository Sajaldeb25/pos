function showName() {
    var name = $('#fullname').val();
    $('#username').text(name);
}

function checkFieldError() {
    if ($('#email_error').length) {
        var emailError = JSON.parse($('#email_error').text());
        $('#email_error_text').text(emailError);
        $('#id_email').addClass('error_border');

    } else {
        emailError = '';
        $('#id_email').removeClass('error_border');
    }
    if ($('#phone_no1_error').length) {
        var phoneNo1error = JSON.parse($('#phone_no1_error').text());
        $('#phone_no1_error_text').text(phoneNo1error);
        $('#id_phone_no1').addClass('error_border');

    } else {
        phoneNo1error = '';
        $('#id_phone_no1').removeClass('error_border');
    }
    if ($('#phone_no2_error').length) {
        var phoneNo2error = JSON.parse($('#phone_no2_error').text());
        $('#phone_no2_error_text').text(phoneNo2error);
        $('#id_phone_no2').addClass('error_border');

    } else {
        phoneNo2error = '';
        $('#id_phone_no2').removeClass('error_border');
    }

    if ($('#name_error').length) {
        var nameError = JSON.parse($('#name_error').text());
        $('#name_error_text').text(nameError);
        $('#fullname').addClass('error_border');
    } else {
        nameError = '';
        $('#fullname').removeClass('error_border');
    }

    if ($('#nid_error').length) {
        var nidError = JSON.parse($('#nid_error').text());
        $('#nid_error_text').text(nidError);
        $('#id_nid').addClass('error_border');
    } else {
        nidError = '';
        $('#id_nid').removeClass('error_border');

    }
    if ($('#city_error').length) {
        var cityError = JSON.parse($('#city_error').text());
        $('#city_error_text').text(cityError);
        $('#id_city').addClass('error_border');
    } else {
        cityError = '';
        $('#id_city').removeClass('error_border');
    }
    if ($('#country_error').length) {
        var countryError = JSON.parse($('#country_error').text());
        $('#country_error_text').text(countryError);
        $('#id_country').addClass('error_border');
    } else {
        countryError = '';
        $('#id_country').removeClass('error_border');
    }
    if ($('#gender_error').length) {
        var genderError = JSON.parse($('#gender_error').text());
        $('#gender_error_text').text(genderError);
        $('#gender').addClass('error_border');
    } else {
        genderError = '';
        $('#gender').removeClass('error_border');
    }
    if ($('#dob_error').length) {
        var dobError = JSON.parse($('#dob_error').text());
        $('#dob_error_text').text(dobError);
        $('#datepicker').addClass('error_border');
    } else {
        dobError = '';
        $('#datepicker').removeClass('error_border');
    }
}

function profilePicPreview(input) {
    var reader = new FileReader();
    reader.onload = (element) => {
         $('#img_preview').attr('src', element.target.result);
    }
    reader.readAsDataURL(input.files[0]);
}

$(document).ready(function () {
    checkFieldError();
    $("#img_input").change(function () {
        profilePicPreview(this);
    });
});