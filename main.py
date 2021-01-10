from server import Server
from settings import PORT, DOMAIN_NAME


def main():
    server = Server(DOMAIN_NAME, PORT)
    print('Starting Floating Chat Server')
    server.start()


if __name__ == '__main__':
    main()
