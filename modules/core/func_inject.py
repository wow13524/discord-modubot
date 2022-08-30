import asyncio

class Module:
    name = "func_inject"

    def __init__(self,bot):
        self.bot = bot
        self.groups = {}

    def inject(self,func,inj_async=True):
        func_name = func.__name__
        if func_name in self.groups:
            self.groups[func_name].append(func)
        else:
            self.groups[func_name] = []
            predefined = False
            try:
                predefined = getattr(self.bot,func_name)
            except:
                pass
            if predefined:
                self.inject(getattr(self.bot,func_name))
            self.inject(func)

            group = self.groups[func_name]
            runner = None
            if inj_async:
                async def runner(*args):
                    await asyncio.wait([x(*args) for x in group])
            else:
                def runner(*args):
                    for x in group:
                        x(*args)
            setattr(self.bot,func_name,runner)