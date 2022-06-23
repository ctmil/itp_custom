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
    date_sale_order_confirm = fields.Datetime('Fecha confirmacion cotizacion')
    days_in_crm = fields.Integer('Dias en CRM',compute="_compute_days_stats")
    days_in_sale = fields.Integer('Dias en Ventas',compute="_compute_days_stats")

    def write(self, vals):
        if 'automated_probability' in vals or 'probability' in vals:
            if vals.get('automated_probability') == 100 or vals.get('probability') == 100:
                vals['date_won'] = str(datetime.now())[:19]
        return super(CrmLead, self).write(vals)

    def _compute_days_stats(self):
        for rec in self:
            res = res1 = 0
            if rec.date_won:
                res = (rec.date_won - rec.create_date).days
            if rec.date_sale_order_confirm:
                order = self.env['sale.order'].search([('opportunity_id','=',rec.id)],limit=1)
                if order:
                    res1 = (rec.date_sale_order_confirm - order.create_date).days
            rec.days_in_crm = res
            rec.days_in_sale = res1

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            if rec.opportunity_id:
                opportunity_id = rec.opportunity_id
                opportunity_id.date_sale_order_confirm = str(datetime.now())[:19]
                opportunity_id.action_set_won()
        return res
