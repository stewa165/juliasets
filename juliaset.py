class JuliaSet(object):
    def __init__(self, c, n=100):
        self.c = c
        self.n = n
        self._d = 0.001
        self._complexplane = []
  
    def juliamap(self, z):
        return (z**2) + self.c
    
    def iterate(self, z):
        m = 0    
        while True:
            z = self.juliamap(z)
            m += 1
            if abs(z) > 2:
                return m
            if m >= self.n:
                return 0  
            
    def setcomplexplane(self):
        numSteps = int(4.0/self._d)#+1
        self.x = [-2+self._d*i for i in xrange(numSteps)]
        self.y = self.x
        self._complexplane = []
        for x in self.x:
            for y in self.y:
                z = x + y*1j
                self._complexplane.append(z)
   
    def set_spacing(self, d):
        self._d = d
        self.setcomplexplane()
        
    def generate(self):
        self.set = []
        for z in self._complexplane:
            self.set.append(self.iterate(z))
        return self.set
        