odoo.define('website_product_store_pickup_knk.custom', function(require) {
    "use strict";
    require('web.dom_ready');
    var core = require('web.core');
    var publicWidget = require('web.public.widget');

    var _t = core._t;

    publicWidget.registry.websiteSaleDeliveryCustom = publicWidget.Widget.extend({
        selector: '.oe_website_sale #delivery_method',
        events: {
            'click .o_delivery_carrier_select': '_onCarrierClick_custom',
            'change .sd_pickup_id': 'sd_pickup_change'
        },
        start: function(){
            $('.sd_pickup_id').each(function () {
                if ($(this).is(':visible')) {
                    $(this).hide();
                }
            });
            return this._super.apply(this, arguments);
        },
        sd_pickup_change: function(ev){
            var self = this;
            var store_id = $(ev.currentTarget).val();
            self._rpc({
                route: '/update/pickup/store',
                params: {
                    'store_id': store_id ? parseInt(store_id): false
                },
            }).then(function(data){
                if (data.success && data.pickup_address) {
                    var datas = data.pickup_address;
                    if ($('#cart_total tbody tr#order_delivery').length > 0){
                        $('#cart_total tbody tr#order_delivery').replaceWith(datas);
                    }else{
                        $('#cart_total tbody tr#empty').after(datas);
                    }
                }
            });
        },
        _onCarrierClick_custom: function(ev){
            var self = this;
            var store_id = false;
            var delivery_id = false;
            delivery_id = $(ev.currentTarget).find("input[name='delivery_type']").val();
            if($(ev.currentTarget).find("select[name='sd_pickup_id']").length){
                store_id = $(ev.currentTarget).find("select[name='sd_pickup_id']").val();
                $(ev.currentTarget).find("select[name='sd_pickup_id']").show();
            }else{
                $('.sd_pickup_id').each(function () {
                    if ($(this).is(':visible')) {
                        $(this).hide();
                    }
                });
            }
            self._rpc({
                route: '/update/shipping/type',
                params: {
                    'delivery_id': delivery_id ? parseInt(delivery_id): false,
                    'store_id': store_id ? parseInt(store_id): false
                },
            }).then(function(data){
                if (data.success && data.cart_delivery) {
                    var datas = data.cart_delivery;
                    if ($('#cart_total tbody tr#order_delivery').length > 0){
                        $('#cart_total tbody tr#order_delivery').replaceWith(datas);
                    }else{
                        $('#cart_total tbody tr#empty').after(datas);
                    }
                }
            });
        }
    });
});