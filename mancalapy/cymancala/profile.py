import pstats
import cProfile
import pyximport
pyximport.install()
import cy

cProfile.runctx("cy.approx_pi()", globals(), locals(), "Profile.prof")
s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()