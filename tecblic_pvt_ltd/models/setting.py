from odoo import api, fields, models, _


class TecblicResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    base_salary = fields.Integer("Salary")
    note = fields.Char("Default")

    def set_values(self):
        res = super(TecblicResConfig, self).set_values()
        self.env['ir.config_parameter'].set_param('tecblic_pvt_ltd.base_salary   ', self.base_salary)
        return res

    @api.model
    def get_values(self):
        res = super(TecblicResConfig, self).get_values()
        value = self.env['ir.config_parameter'].sudo().get_param('tecblic_pvt_ltd.base_salary')
        res.update(
            base_salary=float(value)
        )
        return res
