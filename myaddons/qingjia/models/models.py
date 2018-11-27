# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Qingjd(models.Model):
    _name = 'qingjia.qingjd'

    name = fields.Many2one("res.users", string="申请人", required=True)
    days = fields.Float(string="天数", required=True)
    startdate = fields.Date(string="开始日期", required=True)
    reason = fields.Text(string="请假事由")
    
    def send_qingjd(self):
        self.sended = True
        return self.sended
    
    def confirm_qjd(self):
        self.state = 'confirmed'
        return self.state
