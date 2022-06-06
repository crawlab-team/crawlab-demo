import argparse

from crawlab_demo.actions.cleanup import cleanup
from crawlab_demo.actions.import_demo import import_demo
from crawlab_demo.actions.reimport_demo import reimport_demo

root_parser = argparse.ArgumentParser(description='CLI tool for Crawlab Demo')

root_parser.add_argument('action', help='CLI action')
root_parser.add_argument('--api_address', '-a', help='HTTP URL of API address of Crawlab',
                         default='http://localhost:8000', type=str)
root_parser.add_argument('--username', '-u', help='Username for logging in Crawlab', default='admin',
                         type=str)
root_parser.add_argument('--password', '-p', help='Password for logging in Crawlab', default='admin',
                         type=str)


def main():
    args = root_parser.parse_args()
    if args.action == 'import':
        import_demo()
    elif args.action == 'reimport':
        reimport_demo()
    elif args.action == 'cleanup':
        cleanup()


if __name__ == '__main__':
    main()
