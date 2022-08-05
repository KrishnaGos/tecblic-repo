from odoo import api, fields, models, _


class DepertmentSequence(models.Model):
    _inherit = 'hr.employee'

    seq_name = fields.Char(string="Sequence", readonly=True, required=True, copy=False, index=True,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        print("\n\n\n Create Called")
        print("SELF ===", self)
        print("Vals ===", vals)
        department = self.env['hr.department'].search([('id', '=', vals['department_id'])])
        print("Department ===", department)
        print("NAME ===", department.name)
        if vals.get('seq_name', _('New')) == _('New'):
            if department.name == "Administrator":
                print("\n\n\n Department Condition Administrator")
                vals['seq_name'] = self.env['ir.sequence'].next_by_code('hr.employee.admin')
            elif department.name == "Design":
                print("\n\n\n Design Condition Design")
                vals['seq_name'] = self.env['ir.sequence'].next_by_code('hr.employee.design')
            elif department.name == "Development":
                print("\n\n\n Design Condition Developmentl")
                vals['seq_name'] = self.env['ir.sequence'].next_by_code('hr.employee.development')
            elif department.name == "Business Development Executive":
                print("\n\n\n Design Condition Business Development Executive")
                vals['seq_name'] = self.env['ir.sequence'].next_by_code('hr.employee.bde')


        result = super(DepertmentSequence, self).create(vals)
        return result
