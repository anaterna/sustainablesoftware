import time
import math

print("Starting workload...")
start_time = time.time()

while time.time() - start_time < 10:
    [math.sqrt(i) for i in range(1000000)]  # Some CPU work
    print("h")

print("Workload completed.")
