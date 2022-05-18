odoo.define("choose_your_gift.choose_your_gift", function (require) {
    "use strict";
    require("website_sale.cart");
    const publicWidget = require("web.public.widget");

    publicWidget.registry.websiteSaleCart.include({
        events: _.extend({}, publicWidget.registry.websiteSaleCart.prototype.events, {
            'click .js_gift_wrap_product': '_onGiftProduct',
            'click #add_gift': '_addGiftProduct',
        }),
        _onGiftProduct: function (ev) {
            ev.preventDefault();
            let origin_product_id = $(ev.currentTarget).attr('id')
            let hidden_prod_modal = '#hidden_box_' + origin_product_id
            $(hidden_prod_modal).modal('show');
        },
        _addGiftProduct: function (ev) {
            ev.preventDefault();
            let params = {'product_data': []}
            let origin_product_id = $(ev.currentTarget).attr('data').replace('button-gift_', '')
            let gift_product_inputs = $('#gift-product-data_' + origin_product_id + ' .gift-qty')

            gift_product_inputs.each(function(){
                let quantity = parseInt($(this).val())
                if(quantity > 0){
                    params.product_data.push({
                        'product_id': parseInt($(this).attr('id')),
                        'quantity': quantity,
                        'product_custom_attribute_values': [],
                        'variant_values': [],
                        'no_variant_attribute_values': [],
                        'add_qty': 0,
                        'origin_product_id': parseInt(origin_product_id)
                    })
                }
            })

            this._rpc({
                route: "/shop/cart/update_gift",
                params: params,
            }).then(function (data) {
                if (data.warning) {
                    alert(data.warning);
                    return false;
                }
                return window.location = '/shop/cart';
            });
        },
    })

});
