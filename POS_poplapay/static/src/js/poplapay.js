odoo.define('pos_extended.custom_button', function(require) {
  "use strict";
  var PosBaseWidget = require('point_of_sale.BaseWidget');
  var Screen = require('point_of_sale.screens')
  var pos_model = require('point_of_sale.models');
  var rpc = require('web.rpc')
  var exports = {};
  var core = require('web.core');
  var _t = core._t;
  var _lt = core._lt;
  pos_model.load_fields("pos.order", ["transaction_id", "aviite", "ala", "t_print"]);
  pos_model.load_fields("pos.config", ["url_name", "username", "password", "terminal_id", "hardware_id"]);

  Screen.PaymentScreenWidget.include({
    poplapay_request: function(method, id, params) {
      var order = this.pos.get_order();
      var url_name = order.pos.config.url_name;
      var credentials = order.pos.config.username + ':' + order.pos.config.password;
      var terminal_id = order.pos.config.terminal_id;
      var hardware_id = order.pos.config.hardware_id;
      var c = new WebSocket(
        url_name + terminal_id + '/jsonpos',
        ['jsonrpc2.0', 'x-popla-auth-' + btoa(credentials).replace(/\//g, '_').replace(/\+/g, '-').replace(/=/g, '')]
      );

      var send_data = {
        jsonrpc: '2.0',
        method: method,
        params: params
      }

      if (id) {
        send_data['id'] = id
      }
      // requiest open stages.
      c.onopen = function(event) {
        c.send(JSON.stringify(send_data));
      };
      return c
    },
    renderElement: function() {
      this._super();
    },

    // super call of back-end method and when payment method is selected credit card or debit card then this method used and call to
    // popplapay terminal.
    //
    // all parameters get to the back end.
    finalize_validation: function() {
      var self = this;
      var order = this.pos.get_order();
      var amount_total = this.pos.get_order().get_due();
      var close_session = false
      var api_key = order.pos.config.api_key
      var poplapay_journal_id = this.pos.config.poplapay_journal_id
      var poplaypay_total_amount = 0;
      var cancelled_by_user = false;
      var record_data = order.paymentlines.models
      for (var i = 0; i < record_data.length; i++) {
        if (record_data[i].payment_method.id === poplapay_journal_id[0]) {
          poplaypay_total_amount += record_data[i].amount
        };
      };
      // Get payment requiest sended.
      // if (poplaypay_total_amount) {
      if (order.pos.config.poplapay_journal_id && poplaypay_total_amount){
        var socket = self.poplapay_request('Purchase', order.name, {
          api_key: api_key,
          amount: (poplaypay_total_amount * 100),
          currency: "EUR",
          receipt_id: order.sequence_number,
          no_timeout: true,
          request_result: {
            tokens: true // Possibly in future object with token parameters. Default: false
          }
        })
        var element = document.getElementById("myDIV");
        var btn_pop = document.getElementById("button_popla_cancle");
        element.classList.add("loading");
        btn_pop.classList.add('button_popla')
        btn_pop.style.visibility = 'visible';

        // payment processing time the cancle the payment button call
        this.$('#button_popla_cancle').on('click', function() {
          self.poplapay_request('Abort', false, {});
          element.classList.remove("loading");
          btn_pop.style.visibility = 'hidden';
          btn_pop.classList.remove('button_popla');
          close_session = true;
          cancelled_by_user = true;
        });

        // payment Transaction time any issue or timeout and also payment confirm mesaage get in this method.
        socket.onmessage = function(event) {
          var data = JSON.parse(event.data);
          console.log('message: >', data);
          if (data.method == "_CloseReason" && close_session == false && data.params && !(data.params.error.code == 1)) {
            swal({
                title: _t("Timeout!"),
                text: _t("Session Out"),
                icon: "warning",
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
                    var socket = self.poplapay_request('Abort', false, {});
                    element.classList.remove("loading");
                    btn_pop.style.visibility = 'hidden';
                    btn_pop.classList.remove('button_popla')
                    close_session = true
                    break;
                  case "catch":
                    var socket = self.poplapay_request('Abort', false, {});
                    self.finalize_validation()
                    close_session = true
                    break;
                }
              });
          }
          // when payment transaction is Successfully.
          if (data.response_to == "Purchase") {
            if (data.result && data.result.response_text == 'Approved') {
              // alert("Payment Successfully");
              if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) {
                      this.pos.proxy.printer.open_cashbox();
              }
              order.initialize_validation_date();
              order.finalized = true;
              var data_merchant = data.result.merchant_receipt.text.split("\n");
              var ala_split = data_merchant[5].split(' ')
              var t_split = data_merchant[6].split(': ')

              order['transaction_data'] = data.result;
              order['aviite'] = data_merchant[4].split(': ')[1];
              order['ala'] = ala_split[ala_split.length - 1];
              order['t_print'] = t_split[t_split.length - 1];
              order.set_transaction_data(data.result, data_merchant[4].split(': ')[1], ala_split[ala_split.length - 1], t_split[t_split.length - 1]);

              if (order.is_to_invoice()) {
                  var invoiced = this.pos.push_and_invoice_order(order);
                  this.invoicing = true;

                  invoiced.catch(this._handleFailedPushForInvoice.bind(this, order, false));

                  invoiced.then(function (server_ids) {
                      self.invoicing = false;
                      var post_push_promise = [];
                      post_push_promise = self.post_push_order_resolve(order, server_ids);
                      post_push_promise.then(function () {
                              self.gui.show_screen('receipt');
                      }).catch(function (error) {
                          self.gui.show_screen('receipt');
                          if (error) {
                              self.gui.show_popup('error',{
                                  'title': "Error: no internet connection",
                                  'body':  error,
                              });
                          }
                      });
                  });
              } else {
                  var ordered = self.pos.push_order(order);
                  if (order.wait_for_push_order()){
                      var server_ids = [];
                      ordered.then(function (ids) {
                        server_ids = ids;
                      }).finally(function() {
                          var post_push_promise = [];
                          post_push_promise = self.post_push_order_resolve(order, server_ids);
                          post_push_promise.then(function () {
                                  self.gui.show_screen('receipt');
                              }).catch(function (error) {
                                self.gui.show_screen('receipt');
                                if (error) {
                                    self.gui.show_popup('error',{
                                        'title': "Error: no internet connection",
                                        'body':  error,
                                    });
                                }
                              });
                        });
                  }
                  else {
                    self.gui.show_screen('receipt');
                  }

              }
              swal({
                title: "Done!",
                text: "Payment Successfully!",
                icon: "success",
                button: false,
                timer: 3000
              })
              socket.close();
            } else if ((data.error && data.error.code == 1 && cancelled_by_user)) {
              swal({
                  title: _t("Error!"),
                  text: data.error.message,
                  icon: _t("warning"),
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
                      var socket = self.poplapay_request('Abort', false, {});
                      self.finalize_validation()
                      close_session = true
                      break;
                    case "defualt":
                      var socket = self.poplapay_request('Abort', false, {});
                      element.classList.remove("loading");
                      btn_pop.style.visibility = 'hidden';
                      btn_pop.classList.remove('button_popla')
                      close_session = true
                      break;
                  }
                });
            } else if (cancelled_by_user) {
              swal({
                  title: _t("Error!"),
                  text: data.error.message,
                  icon: _t("warning"),
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
                      var socket = self.poplapay_request('Abort', false, {});
                      self.finalize_validation()
                      close_session = true
                      break;
                    case "defualt":
                      var socket = self.poplapay_request('Abort', false, {});
                      element.classList.remove("loading");
                      btn_pop.style.visibility = 'hidden';
                      btn_pop.classList.remove('button_popla')
                      close_session = true
                      break;
                  }
                });
            }
          }
        }
      } else {
        this._super();
      }
    },

  });
  // add custome field of data order and redirect to back and pos order creation time,
  var _super_Order = pos_model.Order.prototype;
  pos_model.Order = pos_model.Order.extend({
    initialize: function(attributes,options){
      _super_Order.initialize.apply(this, arguments);
      this.transaction_data = this.transaction_data || {};
      this.aviite = this.aviite || '';
      this.ala = this.ala || '';
      this.t_print = this.t_print || '';
    },
    set_transaction_data: function(transaction_data, aviite, ala, t_print){
      console.log('set_transaction_data', transaction_data, aviite, ala, t_print);
      this.transaction_data = transaction_data;
      this.aviite = aviite;
      this.ala = ala;
      this.t_print = t_print;
      this.trigger('change');
    },
    get_transaction_data: function(){
      return {
        'transaction_data': this.transaction_data,
        'aviite': this.aviite,
        'ala': this.ala,
        't_print': this.t_print,
      };
    },
    init_from_JSON: function(json){
      _super_Order.init_from_JSON.apply(this, arguments);
      this.transaction_data = json.transaction_data;
      this.aviite = json.aviite;
      this.ala = json.ala;
      this.t_print = json.t_print;
    },
    export_as_JSON: function() {
      var json_data = _super_Order.export_as_JSON.apply(this, arguments);
        json_data['transaction_data'] = this['transaction_data'];
        json_data['aviite'] = this['aviite'];
        json_data['ala'] = this['ala'];
        json_data['t_print'] = this['t_print'];
      return json_data;
    },
  });
});
