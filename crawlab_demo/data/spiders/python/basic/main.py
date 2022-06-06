import time

from crawlab.entity.result import Result
from crawlab.result import save_items


def main():
    results = [
        Result({'hello': 'world'}),
    ]
    save_items(results)
    time.sleep(5)


if __name__ == '__main__':
    main()
