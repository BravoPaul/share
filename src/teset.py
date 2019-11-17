class Policy(object):
    def __init__(self,e_roi,total_argent):
        self.e_roi = e_roi
        self.total_argent = total_argent
    @classmethod
    def buy(cls,**d):
        print(dir(globals()['Policy']))
        method_call = getattr(globals()['Policy'], d['func'])
        method_call(d = d['d'])

    @classmethod
    def _buy_average(cls,**d):
        print('get in',d['d'])


Policy.

Policy.buy(func='_buy_average',d = 'dd')