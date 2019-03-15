class Parent:
    parentAttr = 100

    def __init__(self):
        print('call parent init')

    def parentMethod(self):
        print('call parent method')

    def setAttr(self, value):
        Parent.parentAttr = value

    def getAttr(self):
        print('call parent get attr')
        return Parent.parentAttr

class Child(Parent):
    def __init__(self):
        print('call child init')

    def childMethod(self):
        print('call child method')

c = Child()
c.childMethod()
c.parentMethod()
c.setAttr(200)
c.getAttr()