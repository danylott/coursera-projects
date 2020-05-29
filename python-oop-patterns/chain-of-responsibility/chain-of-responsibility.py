# class SomeObject:
#     def __init__(self):
#         self.integer_field = 0
#         self.float_field = 0.0
#         self.string_field = ""


class EventGet:
    def __init__(self, value_type):
        self.value_type = value_type


class EventSet:
    def __init__(self, value):
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.value_type == int:
                return obj.integer_field
            else:
                return super().handle(obj, event)

        elif isinstance(event, EventSet):
            if type(event.value) == int:
                obj.integer_field = event.value
            else:
                super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.value_type == float:
                return obj.float_field
            else:
                return super().handle(obj, event)
        elif isinstance(event, EventSet):
            if type(event.value) == float:
                obj.float_field = event.value
            else:
                super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.value_type == str:
                return obj.string_field
            else:
                print(super().handle(obj, event))
        elif isinstance(event, EventSet):
            if type(event.value) == str:
                obj.string_field = event.value
            else:
                super().handle(obj, event)
