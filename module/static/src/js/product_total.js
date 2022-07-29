odoo.define('module.pro_qty', function(require){
"use strict";
    console.log("Code Of Custom Quantity Items");
    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;
    var pos_order = models.load_models('pos.order');
    var pro_qty = models.load_fields('pos.order', 'pro_qty');
    var pro_total = models.load_fields('pos.order', 'pro_total');

    models.Order = models.Order.extend({
        initialize: function(attr, options) {
            var line= _super_order.initialize.apply(this, arguments);
            this.pro_qty = this.orderlines.models.length;
                console.log("Items", this.pro_qty)
            let pro_total = 0;
            let count =0;
            var model= this.orderlines.models;
                for (let i in model){
                        count += 1
                    let qty = model[i].quantity
                    pro_total += qty
                };
                console.log("Quantity", pro_total)
                this.pro_total = pro_total;

        },
    });
});






