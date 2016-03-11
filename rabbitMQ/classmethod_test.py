class ResearchHelperBase(object):

    @staticmethod
    def get_status():
        print "status is"


    @classmethod
    def get_research_feature(cls):
        if cls.__name__ == "VAD":
            return cls
        elif cls.__name__ == "Environment":
            return cls.calculatedFrom
        else:
            return None


class VAD(ResearchHelperBase):

    calculatedFrom = ["MFCCAggrigation"]

class Environment(ResearchHelperBase):

    calculatedFrom = ["video_source"]

class ResearchHelper(object):

    def __new__(cls, *args, **kargs):
        instance = object.__new__(cls, *args, **kargs)
        setattr(instance, "owner", "Weilun")
        return instance

    def __init__(self, a, b):
        self.a = a
        self.b = b
        print "finished with init."

if __name__ == "__main__":
    # rhb = ResearchHelperBase()
    # vad = VAD()
    # env = Environment()
    # rhb.get_status()
    # print vad.get_research_feature()
    # print env.get_research_feature()
    rh = ResearchHelper(2, 3)
    print rh.owner
