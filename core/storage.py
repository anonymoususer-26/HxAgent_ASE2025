class Storage:
    def save_optimal_knowledge(self, path, experience):        
        with open(path, "w+") as file:
            file.write(experience)

    def load_optimal_knowledge(self, path):
        try: 
            with open(path, 'r') as file:
                experience = file.read()
        except:
            experience = ""
        return experience