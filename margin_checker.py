def get_float(prompt):
    while True:
        try:
            return float(input(prompt).strip('% ')) / 100
        except ValueError:
            print("Please enter a valid number or percentage.")

def annualize_return(period_return, period_days):
    # Convert raw return into annualized return using compounding
    return (1 + period_return) ** (365 / period_days) - 1

def margin_analysis():
    print("🔍 Margin Investment Evaluator")
    print("Enter your portfolio returns for the following periods:")

    # Collect user inputs (as percentages)
    r_1d = get_float("1-day return (%): ")
    r_1w = get_float("1-week return (%): ")
    r_1m = get_float("1-month return (%): ")
    r_3m = get_float("3-month return (%): ")
    r_1y = get_float("1-year return (%): ")
    div_yield = get_float("Dividend yield (% per year): ")
    margin_rate = get_float("Annual margin interest rate (%): ")

    # Convert to annualized returns
    a_1d = annualize_return(r_1d, 1)
    a_1w = annualize_return(r_1w, 7)
    a_1m = annualize_return(r_1m, 30)
    a_3m = annualize_return(r_3m, 90)
    a_1y = r_1y  # Already annualized

    # Customizable weights
    weights = {
        '1d': 0.1,
        '1w': 0.2,
        '1m': 0.3,
        '3m': 0.25,
        '1y': 0.15
    }

    weighted_annual_return = (
        a_1d * weights['1d'] +
        a_1w * weights['1w'] +
        a_1m * weights['1m'] +
        a_3m * weights['3m'] +
        a_1y * weights['1y']
    )

    total_expected_return = weighted_annual_return + div_yield
    net_margin_return = total_expected_return - margin_rate

    print("\n📈 Results:")
    print(f"Weighted annualized return (before dividends): {weighted_annual_return * 100:.2f}%")
    print(f"Dividend yield: {div_yield * 100:.2f}%")
    print(f"Total expected return: {total_expected_return * 100:.2f}%")
    print(f"Margin interest rate: {margin_rate * 100:.2f}%")
    print(f"Net return after margin cost: {net_margin_return * 100:.2f}%")

    # Rule of thumb guidance
    if net_margin_return > margin_rate:
        print("✅ This position may justify using margin (2x+ return vs. cost).")
    elif net_margin_return > 0:
        print("⚠️ Marginal benefit. Keep monitoring — you're earning slightly more than cost.")
    else:
        print("❌ Not currently worth margin use. Consider reducing exposure.")

if __name__ == "__main__":
    margin_analysis()
