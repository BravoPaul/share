class Outer(object):

    def createInner(self):
        return Outer.Inner(self)

    class Inner(object):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.outer_instance.somemethod()

        def inner_method(self):
            self.outer_instance.anothermethod()

    def do_with_inner_object(self):
