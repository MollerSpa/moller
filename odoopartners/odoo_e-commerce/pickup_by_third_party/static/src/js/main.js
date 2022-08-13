odoo.define('pickup_by_third_party.allow_third_party',function (require) {
    'use strict';
    require('web.dom_ready');

    const $ajax = require('web.ajax');
    const PaymentForm = require('payment.payment_form');

    PaymentForm.include({
        updateNewPaymentDisplayStatus: function () {
            const self = this;
            self._super.apply(this, arguments);
            const $personCollects = $('#selection_allow_third_party').val();
            if ($personCollects == 'another') {
                $('#form_allow_third_party').show();
            }else {
              $('#form_allow_third_party').hide();
            }    
        },
    })

    $('#selection_allow_third_party').on('change', function(){
        const $personCollects = $('#selection_allow_third_party').val();
        if ($personCollects == 'another') {
            $('#form_allow_third_party').show();
        }else {
          $('#form_allow_third_party').hide();
        }    
    });

    $('#delivery_method').ready(function(){
        $('.o_delivery_carrier_select').click(function(){
            const $deliveryCarrierSelectId = $(this).attr('value');
            $ajax.jsonRpc(
                '/shop/payment/delivery_carrier_selection', 'call', {
                'delivery_type_id': $deliveryCarrierSelectId
            }).then(function (data) {
                const $allowThirdParty = data.allow_third_party;
                if ($allowThirdParty === true){
                    $('#form_pickup_by_third_party').show();
                }else {
                    $('#form_pickup_by_third_party').hide();
                }
            })
        })
    });

    $('button#o_payment_form_pay').bind('click', function (ev) {
        const $personCollects = $('#selection_allow_third_party').val();
        if ($personCollects == '' || $personCollects == 'me') {
            return;
        }
        if($personCollects == 'another'){ 
            const $dict = {'allow_third_party': $personCollects};
            const $thirdPartyName = $('#third_party_name').val();
            const $thirdPartyLastname = $('#third_party_lastname').val();
            const $thirdPartyLastname2 = $('#third_party_lastname2').val();
            const $thirdPartyNameVat = $('#third_party_name_vat').val();
            if($('#third_party_name').length > 0 && $thirdPartyName){
                $dict.third_party_name = $thirdPartyName;
            } else {
                $dict.third_party_name = "";
            }
            if($('#third_party_lastname').length > 0 && $thirdPartyLastname){
                $dict.third_party_lastname = $thirdPartyLastname;
            } else {
                $dict.third_party_lastname = "";
            }
            if($('#third_party_lastname2').length > 0 && $thirdPartyLastname2){
                $dict.third_party_lastname2 = $thirdPartyLastname2;
            } else {
                $dict.third_party_lastname2 = "";
            }
            if($('#third_party_name_vat').length > 0 && $thirdPartyNameVat){
                $dict.third_party_name_vat = $thirdPartyNameVat;
            } else {
                $dict.third_party_name_vat = "";
            }
            $ajax.jsonRpc('/shop/payment/allow_third_party', 'call', $dict);
        }
    });
    
});