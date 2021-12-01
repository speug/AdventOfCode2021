import numpy as np

sonar = np.loadtxt('input')
# part 1
d_sonar = np.diff(sonar)
print(f'Part 1: {np.sum(d_sonar > 0.)}')

# part 2
# convolution with ones is equal to sliding sum
sonar3 = np.convolve(sonar, np.ones(3), 'valid')
d_sonar3 = np.diff(sonar3)
print(f'Part 2: {np.sum(d_sonar3 > 0.)}')
