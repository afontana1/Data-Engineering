class MyClass:
    def method(self):
        return 'instance method called', self 
        # 'self' is replaced and returns the object in memory

    @classmethod
    def classmethod(cls):
        return 'class method called', cls

    @staticmethod
    def staticmethod():
        return 'static method called'


obj = MyClass()
# an instance can call instance method:
obj.method()

# an instance can call its class method:
obj.classmethod()

# an instance can call the class's static method:
obj.staticmethod()

if __name__ == '__main__':
    obj = MyClass()
    # an instance can call instance method:
    obj.method()

    # an instance can call its class method:
    obj.classmethod()

    # an instance can call the class's static method:
    obj.staticmethod()