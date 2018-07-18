class Logger:
    def __init__(self, silent = False):
        self.silent = silent
    
    def log(self, message, important = False):
        if important or not self.silent:
            print(message)
    
    def ask(self, question):
        return input(question + " ")
    
    def ask_yn(self, question, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        
        if default is None:
            prompt = " [y/n]"
        elif default == "yes":
            prompt = " [Y/n]"
        elif default == "no":
            prompt = " [y/N]"
        else:
            raise ValueError("invalid default answer: '%s" % default)
        
        while True:
            choice = self.ask(question + prompt).lower()

            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                self.log("Please respond with 'yes' or 'no (or 'y', 'n' or '[ENTER]').")