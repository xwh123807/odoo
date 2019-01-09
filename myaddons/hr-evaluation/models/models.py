# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.release import description


class Level(models.Model):
    """
        职级，比如p1、p2、m1、m2
    """
    _name = 'hr.level'
    
    name = fields.Char(string='Name', required=True)
    

class Post(models.Model):
    """
        岗位，如开发工程师、测试工程师
    """
    _name = 'hr.post'
    
    name = fields.Char(string='Name', required=True)
    postlevel_ids = fields.One2many('hr.postlevel', "post_id", string='Post Level')
    postskill_ids = fields.One2many('hr.postskill', 'post_id', string='Post Skill')
    skillscore_ids = fields.One2many('hr.skillscore', 'post_id', string='Skill Score')
    postscore_ids = fields.One2many('hr.postscore', 'post_id', string='Post Score')
    postcondition_ids = fields.One2many('hr.postcondition', 'post_id', string='Post Condition')
    postdesc_ids = fields.One2many('hr.postdesc', 'post_id', string='Post Qualification')


class PostLevel(models.Model):
    """
        岗位职级，如首席开发工程师、高级专家开发工程师
    """
    _name = 'hr.postlevel'
    
    name = fields.Char(string='Name', required=True)
    level_id = fields.Many2one("hr.level", string="Level", required=True)
    post_id = fields.Many2one("hr.post", string="Post", required=True)
    description = fields.Text('Description')
    postcondition_ids = fields.One2many('hr.postcondition', 'postlevel_id', string="Post Condition")
    postdesc_ids = fields.One2many('hr.postdesc', 'postlevel_id', string='Post Qualification')
    postscore_ids = fields.One2many('hr.postscore', 'postlevel_id', string='Post Score')
    total_score = fields.Integer('Total Score', compute='_compute_total_score', store=True)
    
    @api.depends('postscore_ids')
    def _compute_total_score(self):
        for line in self:
            line.total_score = sum(line.postscore_ids.mapped('score'))

    
class Skill(models.Model):
    """
        技能，如开发能力、设计能力
    """
    _name = 'hr.skill'
    
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class PostSkill(models.Model):
    """
        岗位技能，定义岗位需要考核的技能
    """
    _name = 'hr.postskill'
    
    post_id = fields.Many2one('hr.post', string='Post', required=True, help='Post');
    skill_id = fields.Many2one('hr.skill', string='Skill', required=True, help='Skill')
    skill_description = fields.Text('Skill Description', related='skill_id.description', readonly=True)


class SkillScore(models.Model):
    """
        技能得分定义
    """
    _name = 'hr.skillscore'
    
    post_id = fields.Many2one("hr.post", string="Post", required=True)
    skill_id = fields.Many2one("hr.skill", string="Skill", required=True)
    score = fields.Integer(string='Score')
    description = fields.Text(string='Description')


class PostCondition(models.Model):
    """
        岗级基本条件
    """
    _name = 'hr.postcondition'
    
    postlevel_id = fields.Many2one('hr.postlevel', string="Post Level", required=True)
    requirement_condition = fields.Text(string='Requirement')
    standard_condition = fields.Text(string='Standard')
    level_id = fields.Many2one('hr.level', string='Level', related='postlevel_id.level_id', readonly=True)
    post_id = fields.Many2one('hr.post', string='Post', related='postlevel_id.post_id', readonly=True, store=True)


class PostDesc(models.Model):
    """
        任职资格描述
    """
    _name = 'hr.postdesc'
    
    postlevel_id = fields.Many2one('hr.postlevel', string="Post Level", required=True)
    skill_id = fields.Many2one('hr.skill', string='Skill', required=True, help='Skill')
    qualification = fields.Text('Qualification')
    level_id = fields.Many2one('hr.level', string='Level', related='postlevel_id.level_id', readonly=True)
    post_id = fields.Many2one('hr.post', string='Post', related='postlevel_id.post_id', readonly=True, store=True)


class PostScore(models.Model):
    """
        任职资格-得分
    """
    _name = 'hr.postscore'
    
    postlevel_id = fields.Many2one('hr.postlevel', string="Post Level", required=True)
    skill_id = fields.Many2one('hr.skill', string='Skill', required=True, help='Skill')
    score = fields.Integer(string='Score')
    post_id = fields.Many2one('hr.post', string='Post', related='postlevel_id.post_id', readonly=True, store=True)
