def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("=== Margin Loan Payoff Table Generator ===")

    # Get basic inputs
    rate = get_float_input("Enter the annual margin interest rate (in %): ") / 100
    borrowed = get_float_input("Enter the amount borrowed: ")

    # Get user preference
    mode = ""
    while mode not in ["1", "2"]:
        print("\nChoose how you'd like to calculate the payoff:")
        print("1. Specify monthly payment amount")
        print("2. Specify number of months to pay off")
        mode = input("Enter 1 or 2: ").strip()

    monthly_rate = rate / 12

    if mode == "1":
        monthly_payment = get_float_input("Enter the amount you want to pay per month: ")

        if monthly_payment <= borrowed * monthly_rate:
            print("⚠️  Monthly payment is too low to cover even the interest. Loan will never be paid off.")
            return

    else:
        months = int(get_float_input("Enter the number of months to pay off: "))
        # Using annuity formula to calculate monthly payment
        if rate == 0:
            monthly_payment = borrowed / months
        else:
            monthly_payment = borrowed * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)

    # Print table
    print("\n{:<6} {:<12} {:<12} {:<12} {:<12}".format("Month", "Payment", "Interest", "Principal", "Balance"))
    print("-" * 60)

    balance = borrowed
    month = 0
    total_interest = 0.0

    while balance > 0:
        month += 1
        interest = balance * monthly_rate
        principal = monthly_payment - interest

        if principal > balance:
            principal = balance
            monthly_payment = interest + principal  # Final payment
        balance -= principal
        total_interest += interest

        print("{:<6} ${:<11.2f} ${:<11.2f} ${:<11.2f} ${:<11.2f}".format(
            month, monthly_payment, interest, principal, balance
        ))

    print("\n✅ Loan paid off in {} months.".format(month))
    print("💸 Total interest paid: ${:.2f}".format(total_interest))


if __name__ == "__main__":
    main()
