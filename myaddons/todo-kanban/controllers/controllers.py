# -*- coding: utf-8 -*-
from odoo import http

# class Todo-kanban(http.Controller):
#     @http.route('/todo-kanban/todo-kanban/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo-kanban/todo-kanban/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo-kanban.listing', {
#             'root': '/todo-kanban/todo-kanban',
#             'objects': http.request.env['todo-kanban.todo-kanban'].search([]),
#         })

#     @http.route('/todo-kanban/todo-kanban/objects/<model("todo-kanban.todo-kanban"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo-kanban.object', {
#             'object': obj
#         })