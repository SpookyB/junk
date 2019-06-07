class LazyTernaryTree(dict):

    def __init__(self, identity):
        self['identity'] = identity
        self['less'] = None
        self['same'] = None
        self['more'] = None

    def eval(self, value):
        if value.startswith(self['identity']):
            return 'same'
        if value < self['identity']:
            return 'less'
        if value > self['identity']:
            return 'more'

    def append(self, value):
        branch = self.eval(value)
        if branch == 'same':
            value = value[len(self['identity']):]
        if self[branch] == None:
            self[branch] = LazyTernaryTree(value)
        else:
            self[branch].append(value)

    def biggest_prefix(self, value, prefix=''):
        branch = self.eval(value)
        if branch == 'same':
            prefix += value[:len(self['identity'])]
            value = value[len(self['identity']):]
        if  self[branch] == None or value == '':
            return prefix
        return self[branch].biggest_prefix(value, prefix) 

    # Utility function, not necessary for the problem domain.
    # def contains(self, value):
    #     branch = self.eval(value)
    #     if branch == 'same':
    #         value = value[len(self['identity']):]
    #     if value == '':
    #         return True
    #     if self[branch] == None:
    #        return False
    #     return self[branch].contains(value)

def ABs(A, B, s):

    B_ = sorted(
        filter(lambda b: b.startswith(s), B),
        key=len)
    A_ = list(filter(lambda b: b.startswith(s), A))

    B_tree = LazyTernaryTree(B_.pop(0))
    for b_ in B_:
        B_tree.append(b_)

    solution = list(filter(lambda a_: B_tree.biggest_prefix(a_) == s, A_))

    print(B_)
    #['ab', 'aba', 'abb', 'abc', 'abaa', 'abab', 'abac', 'abbb', 'abbc', 'abca', 'abcb']
    print(A_)
    #['abef', 'abce', 'abdx', 'abbc']
    print(solution)
    #['abef', 'abdx']

if __name__ == '__main__':
    A = ('abef', 'abce', 'btfx', 'abdx', 'abbc')
    B = ('a', 'b', 'c', 'aa', 'ab', 'ac', 'bb', 'cc', 'aba',
        'abb', 'abc', 'aca', 'acb', 'acc', 'bba', 'bbc', 'cca',
        'abaa', 'abab', 'abac', 'abbb', 'abbc', 'abca', 'abcb')
    s = 'ab'
    ABs(A, B, s)

