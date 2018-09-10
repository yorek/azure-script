from Handler import Handler

class StorageHandler(Handler):
    azure_object = "storage"
 
    def create(self, items):
        cmd = "az"
        cmd += " storage"
        return cmd
 
    def select(self, items):
        pass

    def use(self, items):
        pass