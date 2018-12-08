# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['todo.task', 'mail.thread']
    
    user_id = fields.Many2one('res.users', string='Responsible')
    date_deadline = fields.Date(string='Deadline')
    name = fields.Char(help='Can I help you')
    days = fields.Float('days')
    
    color = fields.Integer('Color Index')
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), (
        '2', 'High')], 'Priority', default='1')
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'),
                                     ('done', 'Read for next stage')], 'Kanban State', default='normal')
    
    @api.multi
    def do_clear_done(self):
        domain = [('is_done', '=', True), '|', ('user_id', '=', self.env.uid), ('user_id', '=', False)]
        done_recs = self.search(domain)
        done_recs.write({'active': False})
        return True
    
    @api.one
    def do_toggle_done(self):
        if self.user_id != self.env.uid:
            raise Exception('Only the reponsiable can do this!')
        else:
            return super(TodoTask, self).do_toggle_done() / 100

    @api.multi
    def action_report_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('todo-all', 'email_template_todo_task')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'todo.task',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })
        return {
            'name': 'Compose Email',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        
