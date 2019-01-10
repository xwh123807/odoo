'''
Created on Jan 10, 2019

@author: xiangwanhong
'''

from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    postlevel_id = fields.Many2one('hr.post', string='Post Level')