from odoo import models, fields, api


class ReviewType(models.Model):
    _name = 'review.type'
    
    name = fields.Char('Name', required=True)

class ReviewProject(models.Model):
    _name = 'review.project'
    
    name = fields.Char('Name')
    leader_uid = fields.Many2one('res.users', string='Leader')
    type_id = fields.Many2one('review.type', string='Type')
#    expert_ids = fields.Many2many('res.users', 'review.experts.rel', 'project_id', 'expert_id', string='Experts')
#    member_ids = fields.Many2many('res.users', 'review.members.rel', 'project_id', 'member_id', string='Member')
    
class ReviewPlan(models.Model):
    _name = 'review.plan'
    