# class PluginMeta(type):
#     def __new__(mcs, name, bases, dct):
#         def register(cls, **kwargs):
#             cls.subclasses.append(cls)
#             super().__init_subclass__(**kwargs)
#
#         plugin = super().__new__(mcs, name, bases, dct)
#         setattr(plugin, "__init_subclass__", register)
#         setattr(plugin, "subclasses", [])
#         return plugin
#
#
# class PluginBase(metaclass=PluginMeta):
#     pass
#
#
# class PluginType1(PluginBase):
#     pass
#
#
# class Plugin2(PluginBase):
#     pass
#
#
# print(PluginType1.subclasses)

# This works nicely
class PluginBase:
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        cls.subclasses.append(cls)
        super().__init_subclass__(**kwargs)
