# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TodoTask(models.Model):
     _name = 'todo.task'
     _inherit = ['todo.task', 'mail.thread']