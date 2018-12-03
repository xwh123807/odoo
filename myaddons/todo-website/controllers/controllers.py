# -*- coding: utf-8 -*-
from odoo import http
from myaddons.todo.models.models import TodoTask

class TodoWebsite(http.Controller):
     @http.route('/hello', auth='public')
     def index(self, **kw):
         return http.request.render('todo-website.hello')
     
     @http.route('/todo-website/todo-website/objects/', auth='public')
     def list(self, **kw):
         return http.request.render('todo-website.listing', {
             'root': '/todo-website/todo-website',
             'objects': http.request.env['todo.task'].search([]),
         })
         
  
     @http.route('/todo-website/todo-website/objects/<model("todo.task"):obj>/', auth='public')
     def object(self, obj, **kw):
         return http.request.render('todo-website.object', {
             'object': obj
         })
         
     @http.route('/todo', auth='public', website=True)
     def index(self, **kwargs):
        TodoTask = http.request.env['todo.task']
        tasks = TodoTask.search([])
        return http.request.render('todo-website.index', {'tasks': tasks})