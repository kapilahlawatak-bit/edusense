import time, random, sys
print("start")
sys.path.insert(0, '.')
import generate_maths_items as g
print("imported")

random.seed(99)
for i in range(200):
    t1 = time.time()
    r = g.build_simple_item()
    dt = time.time() - t1
    if dt > 0.3:
        print(f"SLOW at {i}: {dt:.3f}s")
    if i % 50 == 0:
        print(f"  iteration {i}, elapsed {time.time()-t1:.3f}s")
print("done")
