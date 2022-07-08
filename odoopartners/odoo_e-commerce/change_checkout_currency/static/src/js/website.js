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
                // This is to run minor update as /shop/update_carrier controller (_handleCarrierUpdateResult in js)
                self._handleCheckoutCurrencyUpdateResult(data)
                // window.location.reload();
            });
        },
        _handleCheckoutCurrencyUpdateResult: function (result) {
            var $payButton = $('#o_payment_form_pay');
            var $amountDelivery = $('#order_delivery .monetary_field');
            var $amountUntaxed = $('#order_total_untaxed .monetary_field');
            var $amountTax = $('#order_total_taxes .monetary_field');
            var $amountTotal = $('#order_total .monetary_field, #amount_total_summary.monetary_field');

            if (result.status === true) {
                $amountDelivery.html(result.new_amount_delivery);
                $amountUntaxed.html(result.new_amount_untaxed);
                $amountTax.html(result.new_amount_tax);
                $amountTotal.html(result.new_amount_total);
                var disabledReasons = $payButton.data('disabled_reasons') || {};
                disabledReasons.carrier_selection = false;
                $payButton.data('disabled_reasons', disabledReasons);
                $payButton.prop('disabled', _.contains($payButton.data('disabled_reasons'), true));
            } else {
                $amountDelivery.html(result.new_amount_delivery);
                $amountUntaxed.html(result.new_amount_untaxed);
                $amountTax.html(result.new_amount_tax);
                $amountTotal.html(result.new_amount_total);
            }
        },
    })

});
