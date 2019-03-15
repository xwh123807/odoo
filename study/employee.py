class Employee:
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print('Total employee: %d' % Employee.empCount)

    def displayEmployee(self):
        print('Name: ', self.name, ', Salary: ', self.salary)


emp1 = Employee('test', 'f')
emp2 = Employee('admin', 'm')

print('emp1: ', emp1.displayCount(), emp1.displayEmployee())
print('emp2: ', emp2.displayCount(), emp2.displayEmployee())
emp1.salary = 'fm'
print('emp1: ', emp1.displayCount(), emp1.displayEmployee())