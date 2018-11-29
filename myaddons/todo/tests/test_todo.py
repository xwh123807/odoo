'''
Created on Nov 29, 2018

@author: xiangwanhong
'''
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError


class TestTodo(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super(TestTodo, self).setUp(*args, **kwargs)
        user_demo = self.env.ref('base.user_demo')
        self.env = self.env(user=user_demo)
        print('current user: ', self.user)
        return result

    def test_record_rule(self): 
        "Test per user record rules"
        Todo = self.env['todo.task']
        task = Todo.sudo().create({'name': 'Admin Task'})
        with self.assertRaises(AccessError):
            Todo.browse([task.id]).name
        
