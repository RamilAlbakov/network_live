"""Update network live with GSM cells configured on ENM."""


from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main

load_dotenv('.env')


def main():
    """Update network live with ENM GSM cells."""
    print(enm_main('GSM', truncate=True))


if __name__ == '__main__':
    main()
