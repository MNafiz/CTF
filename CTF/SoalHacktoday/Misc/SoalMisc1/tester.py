from scipy.stats import ortho_group
import time

start = time.time()
mat = ortho_group.rvs(dim=100)
end = time.time()

print(mat[:,1])
print(end-start)