import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, required=True)
    parser.add_argument('--T', type=int, required=True)
    parser.add_argument('--P', type=int, required=True)

    args = parser.parse_args()


