odoo.define("change_checkout_currency.change_checkout_currency", function (require) {
    "use strict";
    const PaymentForm = require('payment.payment_form');

    PaymentForm.include({
        updateNewPaymentDisplayStatus: function () {
            const self = this;
            self._super.apply(this, arguments);
            const $checkedRadio = this.$('input[type="radio"]:checked');

            if ($checkedRadio.length !== 1) {
                return;
            }
            const currency_value = $checkedRadio.parent().find('#currency_payment_id').val()
            if (currency_value === "") {
                return;
            }
            const order_id = parseInt($('.my_cart_quantity').data('order-id'))

            let params = {
                'order_id': order_id,
                'price_list_id': parseInt(currency_value)
            }
            this._rpc({
                route: "/shop/cart/update_currency_checkout",
                params: params,
            }).then(function (data) {
                if (data.equal) {
                    return;
                }
                window.location.reload();
            });
        },
    })

});
