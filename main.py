from datetime import datetime
import smtplib
import requests
import config
import currency
import mail

def main() -> None:
    today = datetime.now()

    try:
        currencies = currency.by_currency(config.def_currency)

        if not currencies:
            print("Error: no exchange rates returned")
            return

        mail.send(currencies, today.strftime("%d/%m/%Y"))
    except ValueError as e:
        print(f"Error: {e}")
    except requests.RequestException as e:
        print(f"Error: could not fetch exchange rates ({e})")
    except (smtplib.SMTPException, OSError) as e:
        print(f"Error: could not send the email ({e})")

if __name__ == "__main__":
    main()
