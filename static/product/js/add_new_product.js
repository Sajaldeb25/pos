function initSize() {
    $('#size_error_text').text('');
    $('#size_input').val('');
    $('#cancel_size').hide();
    $('#size_select').show();
    $('#new_size').show();
    $('#size_input').hide();
    $('#size_select').attr('required', true);
    $('#size_input').attr('required', false);

    $('#new_size').click(() => {
        $('#new_size').hide();
        $('#cancel_size').show();
        $('#size_select').hide();
        $('#size_input').show();
        $('#size_input').attr('required', true);
        $('#size_select').attr('required', false);
    });

    $('#cancel_size').click(() => {
        initSize();
    });
}

// function saveSize(csrftoken, url) {
//     var size = $('#size_input').val();
//     if (size != '') {
//         $.ajax({
//             headers: {
//                 "X-CSRFTOKEN": csrftoken
//             },
//             url: url,
//             method: 'POST',
//             data: {
//                 'size': size
//             },
//             dataType: 'json',
//             success: function (response) {
//                 var size = response.size;
//                 $('#size_select').append(`<option value="${size.id}">${size.size}</option>`);
//                 initSize();
//                 $('#size_success_text').text('Size added successfully');
//                 $('#size_error_text').text('');
//             },
//             error: function (response) {
//                 var error = response["responseJSON"]["error"];
//                 $('#size_error_text').text(error);
//                 $('#size_success_text').text('');
//             }
//         });
//     }
//
// }

function initColor() {
    $('#color_error_text').text('');
    $('#color_input').val('');
    $('#cancel_color').hide();
    $('#color_input').hide();
    $('#color_select').show();
    $('#new_color').show();
    // $('#color_select').attr('required', true);
    $('#color_input').attr('required', false);

    $('#new_color').click(() => {
        $('#new_color').hide();
        $('#cancel_color').show();
        $('#color_select').hide();
        $('#color_input').show();
        $('#color_input').attr('required', true);
        // $('#color_select').attr('required', false);
    });

    $('#cancel_color').click(() => {
        initColor();
    });
}

function initCategory() {
    $('#category_error_text').text('');
    $('#category_input').val('');
    $('#cancel_category').hide();
    $('#category_input').hide();
    $('#category_select').show();
    $('#new_category').show();
    $('#category_input').attr('required', false);
    $('#category_select').attr('required', true);

    $('#new_category').click(() => {
        $('#new_category').hide();
        $('#cancel_category').show();
        $('#category_select').hide();
        $('#category_input').show();
        $('#category_input').attr('required', true);
        $('#category_select').attr('required', false);
    });

    $('#cancel_category').click(() => {
        initCategory();
    });
}

function initProduct() {
    $('#product_error_text').text('');
    $('#product_input').val('');
    $('#cancel_product').hide();
    $('#product_input').hide();
    $('#product_select').show();
    $('#new_product').show();
    $('#product_input').attr('required', false);
    $('#product_select').attr('required', true);
    $('#product_description').hide();
    $('#product_description').val('');

    $('#new_product').click(() => {
        $('#new_product').hide();
        $('#cancel_product').show();
        $('#product_select').hide();
        $('#product_input').show();
        $('#product_input').attr('required', true);
        $('#product_select').attr('required', false);
        $('#product_description').show();
    });

    $('#cancel_product').click(() => {
        initProduct();
    });
}

function checkProductFieldError() {
    if ($('#product_name_error').length) {
        var productNameError = JSON.parse($('#product_name_error').text());
        $('#product_name_error_text').text(productNameError);
        $('#product_input').addClass('error_border');

    } else {
        productNameError = '';
        $('#product_input').removeClass('error_border');
    }
    if ($('#product_description_error').length) {
        var productDescriptionError = JSON.parse($('#product_description_error').text());
        $('#product_description_error_text').text(productDescriptionError);
        $('#descriptionInput').addClass('error_border');

    } else {
        productDescriptionError = '';
        $('#descriptionInput').removeClass('error_border');
    }
    if ($('#supplier_error').length) {
        var productSupplierError = JSON.parse($('#supplier_error').text());
        $('#supplier_error_text').text(productSupplierError);
        $('#supplier_select').addClass('error_border');

    } else {
        productSupplierError = '';
        $('#supplier_select').removeClass('error_border');
    }
    if ($('#category_error').length) {
        var productCategoryError = JSON.parse($('#category_error').text());
        $('#category_error_text').text(productCategoryError);
        $('#category_input').addClass('error_border');

    } else {
        productCategoryError = '';
        $('#category_input').removeClass('error_border');
    }
    if ($('#color_error').length) {
        var productColorError = JSON.parse($('#color_error').text());
        $('#color_error_text').text(productColorError);
        $('#color_input').addClass('error_border');

    } else {
        productColorError = '';
        $('#color_input').removeClass('error_border');
    }

    if ($('#size_error').length) {
        var productSizeError = JSON.parse($('#size_error').text());
        $('#size_error_text').text(productSizeError);
        $('#size_input').addClass('error_border');

    } else {
        productSizeError = '';
        $('#size_input').removeClass('error_border');
    }
    if ($('#bag_purchase_price_error').length) {
        var productPurchaseError = JSON.parse($('#bag_purchase_price_error').text());
        $('#bag_purchase_price_error_text').text(productPurchaseError);
        $('#id_bag_purchase_price').addClass('error_border');

    } else {
        productPurchaseError = '';
        $('#id_bag_purchase_price').removeClass('error_border');
    }
    if ($('#transport_cost_error').length) {
        var productTransportError = JSON.parse($('#transport_cost_error').text());
        $('#transport_cost_error_text').text(productTransportError);
        $('#id_transport_cost').addClass('error_border');

    } else {
        productTransportError = '';
        $('#id_transport_cost').removeClass('error_border');
    }
    if ($('#marketing_cost_error').length) {
        var productMarketingError = JSON.parse($('#marketing_cost_error').text());
        $('#marketing_cost_error_text').text(productMarketingError);
        $('#id_marketing_cost').addClass('error_border');

    } else {
        productMarketingError = '';
        $('#id_marketing_cost').removeClass('error_border');
    }
    if ($('#vat_error').length) {
        var productVatError = JSON.parse($('#vat_error').text());
        $('#vat_error_text').text(productVatError);
        $('#id_vat').addClass('error_border');

    } else {
        productVatError = '';
        $('#id_vat').removeClass('error_border');
    }
    if ($('#printing_error').length) {
        var productPrintingError = JSON.parse($('#printing_error').text());
        $('#printing_error_text').text(productPrintingError);
        $('#id_printing_cost').addClass('error_border');

    } else {
        productPrintingError = '';
        $('#id_printing_cost').removeClass('error_border');
    }
    if ($('#profit_error').length) {
        var productProfitError = JSON.parse($('#profit_error').text());
        $('#profit_error_text').text(productProfitError);
        $('#id_profit').addClass('error_border');

    } else {
        productProfitError = '';
        $('#id_profit').removeClass('error_border');
    }
    if ($('#discount_error').length) {
        var productDiscountError = JSON.parse($('#discount_error').text());
        $('#discount_error_text').text(productDiscountError);
        $('#id_discount_percent').addClass('error_border');

    } else {
        productDiscountError = '';
        $('#id_discount_percent').removeClass('error_border');
    }
    if ($('#discount_min_purchase_error').length) {
        var productDiscountMinError = JSON.parse($('#discount_min_purchase_error').text());
        $('#discount_min_purchase_error_text').text(productDiscountMinError);
        $('#id_discount_min_purchase').addClass('error_border');

    } else {
        productDiscountMinError = '';
        $('#id_discount_min_purchase').removeClass('error_border');
    }
    if ($('#stock_total_error').length) {
        var productStockError = JSON.parse($('#stock_total_error').text());
        $('#stock_total_error_text').text(productStockError);
        $('#id_stock_total').addClass('error_border');

    } else {
        productStockError = '';
        $('#id_stock_total').removeClass('error_border');
    }
}