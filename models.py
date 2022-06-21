from odoo import tools, models, fields, api, _
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'En proceso'),
        ('sent', 'Presupuesto enviado'),
        ('sale', 'Pedido realizado'),
        ('done', 'Ganada'),
        ('cancel', 'Perdida'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_won = fields.Datetime('Fecha ganada')

    def write(self, vals):
        if 'automated_probability' in vals or 'probability' in vals:
            if vals.get('automated_probability') == 100 or vals.get('probability') == 100:
                vals['date_won'] = str(datetime.now())[:19]
        return super(CrmLead, self).write(vals)
