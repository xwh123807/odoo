# -*- coding: utf-8 -*-
from odoo import http

# class Todo-website(http.Controller):
#     @http.route('/todo-website/todo-website/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo-website/todo-website/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo-website.listing', {
#             'root': '/todo-website/todo-website',
#             'objects': http.request.env['todo-website.todo-website'].search([]),
#         })

#     @http.route('/todo-website/todo-website/objects/<model("todo-website.todo-website"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo-website.object', {
#             'object': obj
#         })