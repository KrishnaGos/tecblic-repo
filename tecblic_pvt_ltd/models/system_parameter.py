from odoo import api, fields, models, _


class TecblicSystemParameter(models.TransientModel):
    _inherit = 'res.config.settings'

    base_salary = fields.Integer("Salary")
    allowed_warehouse = fields.Char(string='Allowed Warehouse', config_parameter='allowed_warehouse')





