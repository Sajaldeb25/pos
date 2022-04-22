def generate_pos_invoice(order_details):
    item_row = ''
    for item in order_details.items:
        temp_item_row = """
            <tr class="service">
                <td class="tableitem item-name"><p class="itemtext">{} ({}, {}, {}, {})</p></td>
                <td class="tableitem"><p class="itemtext">{}</p></td>
                <td class="tableitem"><p class="itemtext">{:.3f}</p></td>
            </tr>
        """.format(
            item.product.product.product_name,
            item.product.size.size,
            item.product.color.color if item.product.color else '',
            item.product.gsm,
            item.product.category.category,
            item.quantity,
            item.sub_total
        )
        item_row += temp_item_row

    item_end = """
        <tr class="tabletitle">
            <td></td>
            <td class="Rate"><h2>Total</h2></td>
            <td class="payment"><h2>{:.3f}</h2></td>
        </tr>
        <tr class="tabletitle">
            <td class="Rate"><h2 id="posInvoicePaidDate">Date:{:%d-%m-%Y}</h2></td>
            <td class="Rate"><h2>Paid</h2></td>
            <td class="payment"><h2 id="posInvoicePaid">{:.3f}</h2></td>
        </tr>
         <tr class="tabletitle">
            <td></td>
            <td class="Rate"><h2>Due</h2></td>
            <td class="payment"><h2 id="posInvoiceDue">{:.3f}</h2></td>
        </tr>
    """.format(order_details.total_billed,
               order_details.order_payment_history[
                   0].date if order_details.order_payment_history else order_details.ordered_date,
               order_details.paid_total, order_details.total_due)

    middle_html = item_row + item_end
    invoice_html = get_style() + get_html_first_part() + middle_html + get_html_last_part()

    return invoice_html


def get_style():
    style = """
           <style>
                * {
                   -webkit-print-color-adjust: exact !important; /*Chrome, Safari */
                   color-adjust: exact !important;  /*Firefox*/
               }
               @page {
                 size: portrait;
                 margin:0%;
               }
               #invoice-POS {
                 box-shadow: 0 0 1in -0.25in rgba(0, 0, 0, 0.5);
                 padding: 2mm;
                 margin: 0 auto;
                 width: 44mm;
                 background: #fff;
               }
               #invoice-POS ::selection {
                 background: #f31544;
                 color: #fff;
               }
               #invoice-POS ::moz-selection {
                 background: #f31544;
                 color: #fff;
               }
               #invoice-POS h1 {
                 font-size: 1.5em;
                 color: #222;
               }
               #invoice-POS h2 {
                 font-size: 0.9em;
               }
               #invoice-POS h3 {
                 font-size: 1.2em;
                 font-weight: 300;
                 line-height: 2em;
               }
               #invoice-POS p {
                 font-size: 0.7em;
                 color: #666;
                 line-height: 1.2em;
                 margin: 0px;
                 margin-bottom: 3px;
               }
               #invoice-POS #top,
               #invoice-POS #bot {
                 /* Targets all id with 'col-' */
                 border-bottom: 1px solid #eee;
               }
               #invoice-POS #top {
                 min-height: 100px;
               }
               #invoice-POS #mid {
                 min-height: 80px;
               }
               #invoice-POS #bot {
                 min-height: 50px;
               }
               #invoice-POS #top .logo {
                 height: 60px;
                 width: 60px;
                 background: url(http://michaeltruong.ca/images/logo1.png) no-repeat;
                 background-size: 60px 60px;
               }
               #invoice-POS .info {
                 display: block;
                 margin-left: 0;
                 margin-bottom: 15px;
               }
               .info p{
                 font-size: 8px !important;
               }
               .info h2{
               font-size: 10px !important;
               margin-bottom: 2px !important;
               }
               #invoice-POS .title {
                 float: right;
               }
               #invoice-POS .title p {
                 text-align: right;
               }
               #invoice-POS table {
                 width: 100%;
                 border-collapse: collapse;
               }
               #invoice-POS .tabletitle {
                 font-size: 0.5em;
                 background: #eee;
               }
               #invoice-POS .service {
                 border-bottom: 1px solid #eee;
               }
               #invoice-POS .tableitem {
                 width: 24mm;
               }
               #invoice-POS .itemtext {
                 font-size: 0.5em;
               }
               .item-name{
               padding-right: 5px !important;
           </style>
       """
    return style


def get_html_first_part():
    html = """
          <div id="invoice-POS">
            <center id="top">
              <div class="logo"></div>
              <div class="info"> 
                <h2>Mabjs Enterprise & Printing Press</h2>
                <p>Ramdia Bazar, Baliakandi, Rajbari.</p>
                <p>Proprietor's: Emamul Ehsan Sumon & Abdul Kader Babu</p>
                <p>Contact no: 01315657051, 01723583432</p>
                <hr>
              </div><!--End Info-->
            </center><!--End InvoiceTop-->
            <div id="bot">
                <div id="table">
                    <table>
                        <tr class="tabletitle">
                            <td class="item"><h2>Item</h2></td>
                            <td class="Hours"><h2>Qty</h2></td>
                            <td class="Rate"><h2>Sub Total(BDT)</h2></td>
                        </tr>
    """
    return html


def get_html_last_part():
    html = """
                </table>
            </div><!--End Table-->
        </div><!--End InvoiceBot-->
      </div><!--End Invoice-->
    """
    return html
