class First(object):
    def __init__(self):
        print "first"

class Second(First):
    def __init__(self):
        print "second"

class Third(First):
    def __init__(self):
    	super(Third, self).__init__()
        print "third"

class Fourth(Third, Second):
    def __init__(self):
        super(Fourth, self).__init__()
        print "that's it"


fourth = Fourth()
print Fourth.__mro__
#super(Fourth,fourth).__init__()
