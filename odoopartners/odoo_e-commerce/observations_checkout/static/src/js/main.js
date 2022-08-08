odoo.define('observations_checkout.checkout_observations',function (require) {
    'use strict';
    require('web.dom_ready');
    const ajax = require('web.ajax');
    
    $("button#o_payment_form_pay").bind("click", function (ev) {
        const checkout_observations = $('#checkout_observations').val();
        if($('#checkout_observations').length > 0 && checkout_observations){
            ajax.jsonRpc('/checkout_observations', 'call', {
                'checkout_observations': checkout_observations
            })
        }
    });
});