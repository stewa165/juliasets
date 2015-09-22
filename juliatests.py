from juliaset import JuliaSet
from random import uniform, randint
from math import sqrt
from nose import with_setup

###
# Test Suite for specified JuliaSet interface
#
# Run with the command: "nosetests juliatests.py"
###


# Custom random numbers

def rand_range():
    """Return a random complex number bounded by real and imaginary axes [-2, 2]"""
    return (uniform(-2,2) + uniform(-2,2)*1j)

def rand_circle():
    """Return a random complex number within the unit circle"""
    r = uniform(-1,1)
    dr = sqrt(1 - r**2)
    i = uniform(-dr, dr)
    return (r + i*1j)

# Test classes for several cases
    
class TestRandomC:
    """Define a julia set with a random c seed value, test interface"""
    
    def setup(self):
        """Setup fixture is run before every test method separately"""
        self.c = rand_range()
        self.n = randint(2,100)
        self.j = JuliaSet(self.c, self.n)
        
    def test_c_value(self):
        """Test that c is an attribute"""
        assert self.j.c == self.c
    
    def test_n_value(self):
        """Test that n is an attribute"""
        assert self.j.n == self.n
        
    def test_juliamap(self):
        """Test that juliamap is implemented properly"""
        z = rand_range()
        print "z = ", z
        print "z**2 = ", z**2
        zcorrect = z**2 + self.c
        print "z**2 + c = ", zcorrect
        znew = self.j.juliamap(z)
        print "juliamap(z) = ", znew
        assert znew == zcorrect
    
    def test_set_spacing(self):
        """Test that changing spacing works"""
        print "Test original spacing _d = 0.001"
        assert self.j._d == 0.001
        print "Test new spacing of _d = 0.1"
        self.j.set_spacing(0.1)
        print "_d = ", self.j._d
        assert self.j._d == 0.1
        print "Test that complex plane is regenerated"
        print "len(_complexplane) = ", len(self.j._complexplane)
        print "int(4.0 / 0.1) = ", int(4.0 / 0.1)**2
        assert len(self.j._complexplane) == int(4.0 / 0.1)**2
    
    def test_generate(self):
        """Test that generating the julia set works"""
        self.j.set_spacing(0.1)
        s = self.j.generate()
        print "Test that j.set exists, and is of the same length as j._complexplane"
        assert (self.j.set == s) and (len(self.j.set) == len(self.j._complexplane))

class TestTrivial:
    """Test that a seed value of c=0 leaves the unit circle invariant"""
    
    @classmethod
    def setup_class(cls):
        cls.j = JuliaSet(0)
    
    def test_trivial_seed(self):
        def check_z(z):
            """Test all z inside unit circle return 0"""
            m = TestTrivial.j.iterate(z)
            print "m = ", m
            assert m == 0
        # A generator like this runs a test for every yield
        for _ in xrange(100):
            z = rand_circle()
            yield check_z, z

class TestHuge:
    """Test that a huge seed always causes a divergence after 1 iteration"""
    
    @classmethod
    def setup_class(cls):
        cls.j = JuliaSet(16)
    
    def test_huge_seed(self):
        def check_z(z):
            """Test all z escape after 1 iteration"""
            print "z = ", z
            print "z^2 = ", z**2
            print "z^2 + c = ", z**2 + 16
            print "juliamap(z) = ", TestHuge.j.juliamap(z)
            assert TestHuge.j.iterate(z) == 1
        # Again, a generator runs a test for every yield
        for _ in xrange(100):
            z = rand_range()
            yield check_z, z
        