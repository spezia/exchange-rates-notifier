from datetime import datetime
import sys
import config

if config.BASE_DIR not in sys.path:
    sys.path.append(config.BASE_DIR)

import currency
import mail

def main():
    currencies = currency.by_currency(config.def_currency)
    today = datetime.now()

    if currencies:
        mail.send(currencies, today.strftime("%d/%m/%Y"))

if __name__ == "__main__":
    main()
