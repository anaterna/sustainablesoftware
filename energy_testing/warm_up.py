import time

def warm_up(duration=60):
    end_time = time.time() + duration
    while time.time() < end_time:
        _ = [x**2 for x in range(10000)]

def main():
    print("Warming up...")
    warm_up()

if __name__ == "__main__":
    main()

