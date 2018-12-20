class RedflagData:
    def __init__(self):
        self.redflags_list = []

    def create_redflag(self, redflag):  
        return self.redflags_list.append(redflag)

    def get_redflags(self):
        return self.redflags_list

    def get_redflag(self, redflag_id):
        for redflag in self.redflags_list:
            if redflag.get("redflag_id") == redflag_id:
                return redflag
        return None

    def update_redflag(self, redflag_id, new_update):
        for redflag in self.redflags_list:
            if redflag.get("redflag_id") == redflag_id:
                redflag.update(new_update)
                return redflag
        return None

    def delete_redflag(self, redflag_id):
        for redflag in self.redflags_list:
            if redflag.get("redflag_id") == redflag_id:
                self.redflags_list.remove(redflag)
                return redflag
        return None