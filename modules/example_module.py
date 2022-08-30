class Module:
    name = "example_module"

    def __init__(self,bot):
        """
        Initialize any necessary instance variables for the module.
        """

    async def init(self):
        """
        Interface with the bot after the client has been initialized.
        """
    
    async def postinit(self):
        """
        Interface with other modules after they have been initialized.
        """