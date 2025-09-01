import argparse
import datetime
import math
import os

script_name = os.path.basename(__file__)
FREQ_OPTIONS = {
    '1': ('Weekly', 7),
    '2': ('Biweekly', 14),
    '3': ('Monthly', 30),
    '4': ('Custom', None),
    '0': ('Exit', None),
}

def generate_schedule(balance, frequency_days, deployments, cash_apy, market_apy):
    cash_rate = (1 + cash_apy / 100) ** (frequency_days / 365) - 1
    market_rate = (1 + market_apy / 100) ** (frequency_days / 365) - 1

    if cash_rate > 0:
        payment = balance / ((1 - (1 + cash_rate) ** -deployments) / cash_rate)
    else:
        payment = balance / deployments

    schedule = []
    today = datetime.date.today()
    brokerage_balance = 0.0

    for i in range(deployments):
        cash_interest = balance * cash_rate
        balance += cash_interest

        withdraw = min(payment, balance)
        balance -= withdraw
        brokerage_balance += withdraw

        brokerage_growth = brokerage_balance * market_rate
        brokerage_balance += brokerage_growth

        schedule.append({
            'date': today + datetime.timedelta(days=frequency_days * i),
            'withdraw': round(withdraw, 2),
            'cash_interest': round(cash_interest, 2),
            'cash_balance': round(balance, 2),
            'brokerage_deposit': round(withdraw, 2),
            'brokerage_growth': round(brokerage_growth, 2),
            'brokerage_balance': round(brokerage_balance, 2),
        })

        if balance <= 0:
            break

    return schedule

def print_schedule(schedule):
    print(f"\n{'Date':<12} {'Withdraw':>10} {'Cash Int.':>10} {'Cash Bal.':>10} {'Broker Dep.':>12} {'Mrkt Grwth':>12} {'Brkg Bal.':>12}")
    for entry in schedule:
        print(f"{entry['date']} "
              f"{entry['withdraw']:>10.2f} "
              f"{entry['cash_interest']:>10.2f} "
              f"{entry['cash_balance']:>10.2f} "
              f"{entry['brokerage_deposit']:>12.2f} "
              f"{entry['brokerage_growth']:>12.2f} "
              f"{entry['brokerage_balance']:>12.2f}")
    print()

def parse_cli():
    script_name = os.path.basename(__file__)
    parser = argparse.ArgumentParser(
            description=f"Cash Deployment Scheduler\nUsage: python {script_name} [options]"
    )

    parser.add_argument("--balance", type=float, help="Total balance to deploy")
    parser.add_argument("--frequency", choices=["weekly", "biweekly", "monthly", "custom"], help="Deployment frequency")
    parser.add_argument("--custom-days", type=int, help="Custom frequency in days (required if frequency is custom)")
    parser.add_argument("--cash-apy", type=float, help="Annual interest rate on undeployed cash")
    parser.add_argument("--market-apy", type=float, help="Expected market annual return")
    parser.add_argument("--duration", type=int, default=365, help="Deployment duration in days (default: 365)")
    return parser.parse_args()

def main():
    args = parse_cli()

    print("\n=== Cash Deployment Scheduler ===")
    balance = args.balance if args.balance is not None else float(input("Enter total balance to deploy: $"))

    if args.frequency:
        freq_name = args.frequency
        if freq_name == "custom":
            if args.custom_days is None:
                frequency_days = int(input("Enter custom interval in days: "))
            else:
                frequency_days = args.custom_days
        else:
            freq_map = {
                "weekly": 7,
                "biweekly": 14,
                "monthly": 30
            }
            frequency_days = freq_map[freq_name]
    else:
        print("Choose deployment frequency:")
        for key, (label, _) in FREQ_OPTIONS.items():
            print(f"{key}. {label}")
        choice = input("Select option: ").strip()
        if choice not in FREQ_OPTIONS or choice == '0':
            print("Exiting.")
            return
        label, frequency_days = FREQ_OPTIONS[choice]
        if frequency_days is None:
            frequency_days = int(input("Enter custom interval in days: "))
        freq_name = label.lower()

    duration = args.duration
    deployments = math.ceil(duration / frequency_days)
    cash_apy = args.cash_apy if args.cash_apy is not None else float(input("Enter expected annual interest rate for cash: "))
    market_apy = args.market_apy if args.market_apy is not None else float(input("Enter expected annual market yield: "))

    schedule = generate_schedule(balance, frequency_days, deployments, cash_apy, market_apy)
    print_schedule(schedule)

    print("\n# To reproduce this run:")
    cmd = f"python {script_name} --balance {balance} --frequency {freq_name}"

    if freq_name == "custom":
        cmd += f" --custom-days {frequency_days}"
    if cash_apy:
        cmd += f" --cash-apy {cash_apy}"
    if market_apy:
        cmd += f" --market-apy {market_apy}"
    if args.duration != 365:
        cmd += f" --duration {duration}"
    print(cmd)

if __name__ == "__main__":
    main()
