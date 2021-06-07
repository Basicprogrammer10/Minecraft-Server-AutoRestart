class plugin():
    def __init__(self):
        self.name = 'Example Plugin'
        self.version = '1.0'
        self.doRun = False

    # Use Type Annotation to define regex to run this on
    def okKill(self, webhook, text) -> "\[.*\]: \[.*: Killed .*\]":
        # Return a command to have the server run
        return '/say Hm...\n'