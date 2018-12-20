class RedflagData:
    def __init__(self):
        self.redflags_list = []

    def create_redflag(self, redflag):  
        return self.redflags_list.append(redflag)

    def get_redflags(self):
        return self.redflags_list