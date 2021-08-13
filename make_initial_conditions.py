import rebound

for i in range(1, 10):
    sim = rebound.Simulation()
    sim.add(m=1.)
    sim.add(a=i)
    sim.save('data/binaries/run{0:04d}.bin'.format(i))
