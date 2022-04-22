var grandTotal = 0.000;
function calculateGrandTotal() {
    var grandTotal = 0;
    var nancount = 0;
    var rowCount = 0;
    $(".sub_total").each(function () {
        var tempSubTotal = parseFloat($(this).text());
        if (!isNaN(tempSubTotal)) {
            grandTotal += tempSubTotal;
        } else {
            nancount++;
        }
        rowCount++;
    });
    if (rowCount == 0) {
        grandTotal = NaN;
    }
    return {grandTotal, nancount};
}

function disableOrEnablePaidetotalField() {
    var grandTotal = calculateGrandTotal();
    if (!isNaN(grandTotal.grandTotal)) {
        $('#grand_total').text(grandTotal.grandTotal.toFixed(2));
        if (grandTotal.nancount > 0) {
            $('#paid_total_field').attr('disabled', true);
            $('#paid_total_field').val('')
            $('#total_due').text('----');
        } else {
            $('#paid_total_field').removeAttr('disabled');
        }
        $('#paid_total_field').attr('max', grandTotal.grandTotal.toFixed(2));
    } else {
        $('#grand_total').text('----');
        $('#paid_total_field').attr('disabled', true);
        $('#paid_total_field').val('');
        $('#total_due').text('----');
    }
}

function onChangeQuantity(quantityField) {
    var $row = quantityField.closest("tr");
    var $tds = $row.find("td");
    var price = parseFloat($($tds[6]).text()).toFixed(2);
    var quantity = parseInt(quantityField.val());
    var discount = parseInt(quantityField.data('discount'));
    var minPurchase = parseInt(quantityField.data('min-purchase'));
    var subTotal = 0.000;
    var stockTotal = parseInt(quantityField.data('stock-total'));
    if (!isNaN(quantity)) {
        if (quantity >= 0 && quantity <= stockTotal) {
            quantityField.val(quantity);
            quantityField.removeClass('error_border');
        } else if (quantity > stockTotal) {
            quantity = stockTotal;
            quantityField.val(stockTotal);
        } else {
            quantity = 1;
            quantityField.val(1);
        }

        if (quantity >= minPurchase && minPurchase != 0 && discount != 0) {
            subTotal = ((quantity * price) * (1.00 - (discount / 100.000))).toFixed(2);
            $($tds[7]).find('input').attr('value', discount);
            $($tds[7]).find('span').text(discount);
        } else {
             $($tds[7]).find('input').attr('value', 0);
            $($tds[7]).find('span').text(0);
            subTotal = (quantity * price).toFixed(2);
        }
        $($tds[9]).text(subTotal);
    } else {
        quantityField.addClass('error_border');
        $($tds[9]).text('----');
    }
    disableOrEnablePaidetotalField();
}

function addInvoiceItem(productVariant, currentObject) {
    $(currentObject).addClass('avoid-clicks');
    let currId = $(currentObject).attr('id');
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#empty_form_product :input').attr('value', productVariant.variant_id);
    $('#empty_form_price_per_product :input').attr('value', productVariant.price);
    $('#empty_form_discount_percent :input').attr('value', productVariant.discount_percent);
    $('#empty_form_quantity :input').attr({
        'onchange': 'onChangeQuantity($(this))',
        'onkeyup': 'onChangeQuantity($(this))',
        'data-discount': productVariant.discount_percent,
        'data-min-purchase': productVariant.discount_min_purchase,
        'data-stock-total': productVariant.stock_total,
        'max': productVariant.stock_total,
    });
    var newInvoiceItem = '<tr class="nopadding invoice_row" style="cursor: pointer" id="invoice-item-' + productVariant.variant_id + '"  data-parent-id=' + currId + ' oncontextmenu="invoiceContextMenu()">' +
        '<td>' + $('#empty_form_product').html() + '<span>' + productVariant.variant_id + '</span>' + '</td>'
        + '<td>' + productVariant.product_name + '</td>'
        + '<td>' + productVariant.category + '</td>'
        + '<td>' + productVariant.gsm + '</td>'
        + '<td>' + productVariant.size + '</td>'
        + '<td>' + productVariant.color + '</td>'
        + '<td>' + $('#empty_form_price_per_product').html() + '<span>' + productVariant.price + '</span>' + '</td>'
        + '<td>' + $('#empty_form_discount_percent').html() + '<span>' + 0 + '</span>' + '</td>'
        + '<td style="width: 10%;">' + $('#empty_form_quantity').html() + '</td>'
        + '<td class="text-right sub_total">----</td>'
        + '</tr>';
    newInvoiceItem = newInvoiceItem.replace(/__prefix__/g, form_idx);
    $('#invoice_item').append(newInvoiceItem);
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);

    invoiceContextMenu();
    disableOrEnablePaidetotalField();
}

function checkTableEmpty() {
    $(document).bind('DOMSubtreeModified', '#invoice_item', function () {
        if ($('#invoice_item').children().length <= 1) {
            $('#invoice_empty_msg').css('display', 'contents');
        } else {
            $('#invoice_empty_msg').css('display', 'none');
        }
    })
}

function paidTotalInputFieldChange() {
    $('#paid_total_field').bind('change keyup', function () {
        var paidTotal = parseFloat($('#paid_total_field').val());
        var grandTotal = calculateGrandTotal();
        if (!isNaN(paidTotal) && !isNaN(grandTotal.grandTotal)) {
            var due = grandTotal.grandTotal - paidTotal;
            if (due >= 0 && due <= grandTotal.grandTotal) {
                $('#total_due').text(due.toFixed(2));
                $('#paid_total_field').removeClass('error_border');
            } else if (due > grandTotal.grandTotal) {
                $('#paid_total_field').val(0);
                $('#total_due').text(grandTotal.grandTotal.toFixed(2));
            } else {
                $('#paid_total_field').val(grandTotal.grandTotal.toFixed(2));
                $('#total_due').text('0.000');
            }
        } else {
            $('#total_due').text('----');
            $('#paid_total_field').addClass('error_border');
        }
    });
}

function invoiceContextMenu() {
    $('.invoice_row').on('contextmenu', function (e) {
        e.preventDefault();
        $('#contextMenu').css({
            top: e.pageY + 'px',
            left: e.pageX + 'px'
        }).addClass('is-open');
        var parentId = $(this).attr('data-parent-id');
        var currId = $(this).attr('id');
        $('#remove-button').data('invoice-parent-row', parentId);
        $('#remove-button').data('invoice-item-row', currId);
    })
}

function removeInvoiceItem(currObj) {
    var parentId = $('#remove-button').data('invoice-parent-row');
    var curId = $('#remove-button').data('invoice-item-row');
    $('#' + parentId).removeClass('avoid-clicks');
    $('#' + curId).remove();
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) - 1);
    var grandTotal = calculateGrandTotal();
    disableOrEnablePaidetotalField();
    $('#paid_total_field').removeClass('error_border');
    if (!isNaN(grandTotal.grandTotal)) {
        $('#paid_total_field').change();
    }

}

function printPosInvoice(html) {
    html = html.slice(1, -1);
    var myWindow = window.open('', 'Receipt', 'height=400,width=600');
    myWindow.document.write('<html><head><title>Receipt</title>');
    myWindow.document.write('<style type="text/css"> *, html {margin:0;padding:0;} </style>');
    myWindow.document.write('</head><body>');
    myWindow.document.write(html);
    myWindow.document.write('</body></html>');
    myWindow.document.close();
    myWindow.onload = function () {
        myWindow.focus();
        myWindow.print();
        myWindow.close();
    };
}

function initNewCustomer() {
    $('#new_customer').addClass('display-none');
    $('#cancel_new_customer').removeClass('display-none');
    $('#customer_select').val('');
    $('#customer_select').attr('required', false);
    $('#customer_select').addClass('display-none');


    $('#new_customer_name').removeAttr('hidden');
    $('#new_customer_name').attr('required', true);

    $('#customer_phone').removeClass('display-none');
    $('#customer_phone :input').attr('required', true);

    $('#customer_address').removeClass('display-none');
}

function initInitialOrderForm() {
    $('#customer_phone_error_text').text('');
    $('#new_customer_phone').removeClass('error_border');

    $('#new_customer').removeClass('display-none');
    $('#cancel_new_customer').addClass('display-none');
    $('#customer_select').removeClass('display-none');
    $('#customer_select').attr('required', true);

    $('#new_customer_name').val('');
    $('#new_customer_name').attr('hidden', true);
    $('#new_customer_name').removeAttr('required');

    $('#customer_phone :input').val('');
    $('#customer_phone').addClass('display-none');
    $('#customer_phone :input').removeAttr('required');

    $('#customer_address').find('textarea').val('');
    $('#customer_address').addClass('display-none');
}

