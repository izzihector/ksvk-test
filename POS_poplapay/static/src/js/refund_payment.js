odoo.define('POS_poplapay.refund_poplapay_odoo', function (require) {
"use strict";

var core = require('web.core');
var rpc = require('web.rpc')
var framework = require('web.framework');
var core = require('web.core');
var _t = core._t;
var _lt = core._lt;
// system thou send requiest to the poplapay Payment terminal method
function poplapay_request(method, id, params) {
  var c = new WebSocket(
  params['url_name'] + params['terminal_id'] + '/jsonpos',
    [ 'jsonrpc2.0', 'x-popla-auth-' + btoa(params['credentials']).replace(/\//g, '_').replace(/\+/g, '-').replace(/=/g, '') ]
  );
  var send_data = {
    jsonrpc: '2.0',
    method: method,
    params: params
  }
  if(id){
    send_data['id'] = id
  }
  // requiest open stages.
  c.onopen = function (event) {
    c.send(JSON.stringify(send_data));
  };
  return c
}
// all parameters get to the back end.
function RefundPop(parent, action){
  var self = this
  var params = action.params || {};
  var url_name = params.url_name;
  var terminal_id = params.terminal_id
  var wiz_id = params.wiz_id;
  var active_id = params.active_id;
  var credentials = params.username + ':' + params.password;
  var close_session = false
  var cancelled_by_user = false

// refund payment requiest sended.
  var socket = new poplapay_request('Refund', '221', {
    api_key: params.api_key,
    url_name: url_name,
    credentials: credentials,
    terminal_id: terminal_id,
    receipt_id: params.receipt_id,  // mandatory, for Refund (does not match orig Purchase)
    amount: params.amount,
    currency: "EUR",
    transaction_id: params.transaction_id,
    preferred_receipt_text_width: 40,
    external_data: {
          name: params.external_data.name,
          shift: {
          number: 123
          }
    }})
  var element = document.getElementById("div_refund");
  var btn_pop = document.getElementById("button_refund_cancle");
  element.classList.add("loading");
  btn_pop.classList.add('button_popla_refund')
  btn_pop.style.visibility='visible';

  // payment processing time the cancle the payment button call
  $('#button_refund_cancle').on('click', function(){
    new poplapay_request('Abort', false, {
      url_name: url_name,
      credentials: credentials,
      terminal_id: terminal_id,
    });
    element.classList.remove("loading");
    btn_pop.style.visibility='hidden';
    btn_pop.classList.remove('button_popla_refund');
    close_session = true;
    cancelled_by_user = true;
  });

  // payment Transaction time any issue or timeout and also payment confirm mesaage get in this method.
  socket.onmessage = function(event) {
    var data =  JSON.parse(event.data);
    // when terminal session out.
    if (data.method == "_CloseReason" && close_session == false && data.params && !(data.params.error.code == 1)){
      swal({
        title: _t("Timeout!"),
        text: _t("Session Out"),
        icon: _t("warning"),
        buttons: {
          defualt: {
            text: _t("Cancel!"),
            value: "defualt",
          },
          catch: {
            text: _t("Confirm!"),
            value: "catch",
          },
        },
      })
      .then((value) => {
        switch (value) {
          case "defualt":
                new poplapay_request('Abort', false, {
                  url_name: url_name,
                  credentials: credentials,
                  terminal_id: terminal_id,
                });
                element.classList.remove("loading");
                btn_pop.style.visibility='hidden';
                btn_pop.classList.remove('button_popla_refund');
                close_session = true
                // framework.unblockUI();
                break;
          case "catch":
                new poplapay_request('Abort', false, {
                  url_name: url_name,
                  credentials: credentials,
                  terminal_id: terminal_id,
                });
                new RefundPop(parent, action)
                close_session = true
                break;
      }});
    }
    // when payment transaction is Successfully.
    if (data.response_to == "Refund") {
      if (data.result && data.result.response_text == 'Approved'){
          swal({
            title: _t("Done!"),
            text: _t("Payment Successfully!"),
            icon: "success",
            button: false,
            timer: 3000
          })
          rpc.query({
                model: 'pos.make.payment',
                method: 'get_refund_data',
                args: [[wiz_id], {'wiz_id': wiz_id, 'active_id': active_id, 'refund_data': data.result}],
            }).then(function (returned_value){
              location.reload();
            })
            close_session = true
      // when privious transaction running and also invelid transaction get this method and display popup error.
      }else if((data.error && data.error.code == 1) && cancelled_by_user){
          swal({
            title: _t("Error!"),
            text: data.error.message,
            icon: "warning",
            buttons: {
              defualt: {
                text: _t("Cancel!"),
                value: "defualt",
              },
              catch: {
                text: _t("Confirm!"),
                value: "confirm",
              },
            },
          })
          .then((value) => {
            switch (value) {
              case "confirm":
                new poplapay_request('Abort', false, {
                  url_name: url_name,
                  credentials: credentials,
                  terminal_id: terminal_id,
                });
                new RefundPop(parent, action)
                close_session = true
                break
              case "defualt":
                var socket = new poplapay_request('Abort', false, {
                  url_name: url_name,
                  credentials: credentials,
                  terminal_id: terminal_id,
                });
                element.classList.remove("loading");
                btn_pop.style.visibility='hidden';
                btn_pop.classList.remove('button_popla_refund');
                // framework.unblockUI();
                close_session = true
                break
          }});
      // any transaction payment error handling.
      }else{
        swal({
          title: _t("Error!"),
          text: data.error.message,
          icon: "warning",
          buttons: {
            defualt: {
              text: _t("Cancel!"),
              value: "defualt",
            },
            catch: {
              text: _t("Confirm!"),
              value: "confirm",
            },
          },
        })
        .then((value) => {
          switch (value) {
            case "confirm":
              new poplapay_request('Abort', false, {
                url_name: url_name,
                credentials: credentials,
                terminal_id: terminal_id,
              });
              new RefundPop(parent, action)
              close_session = true
              break
            case "defualt":
              var socket = new poplapay_request('Abort', false, {
                url_name: url_name,
                credentials: credentials,
                terminal_id: terminal_id,
              });
              element.classList.remove("loading");
              btn_pop.style.visibility='hidden';
              btn_pop.classList.remove('button_popla_refund');
              // framework.unblockUI();
              close_session = true
              break
        }});
      }
    }
  }
}
// fetch the data of back end
core.action_registry.add('refund_pop', RefundPop);
})
