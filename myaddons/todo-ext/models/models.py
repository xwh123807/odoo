# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TodoTask(models.Model):
#     _name = 'todo.task'
#     _inherits = ['todo.task', 'mail.thread']
    _inherit = 'todo.task'
    
    user_id = fields.Many2one('res.users', string='Responsible')
    date_deadline = fields.Date(string='Deadline')
    name = fields.Char(help='Can I help you')
    
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
            return super(TodoTask, self).do_toggle_done()
        
