import sys

from simulation import Simulation


def main():
    sim = Simulation(sys.argv[1] if len(sys.argv) > 1 else 1)
    sim.run()


if __name__ == "__main__":
    main()
