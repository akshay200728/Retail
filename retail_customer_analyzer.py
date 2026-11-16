"""
PS 80 - Retail Customer Analyzer
Language : Python 3
Concepts : Pandas, Filtering, Grouping, Statistics

Reads customers.csv and provides:
  1. Spending statistics (mean, median, highest, lowest)
  2. High-value customers (TotalSpent >= limit entered by the user)
  3. City-wise summary (total and average spending)
"""

import sys
import pandas as pd  # type: ignore[reportMissingModuleSource]

CSV_FILE = "customers.csv"
REQUIRED_COLUMNS = ["CustomerID", "Name", "City", "Purchases", "TotalSpent"]


def fmt(value):
    """Show whole numbers without decimals (25000), others with 2 decimals."""
    value = float(value)
    return str(int(value)) if value.is_integer() else f"{value:.2f}"


def load_data(filename=CSV_FILE):
    """Load the CSV with Pandas; handle missing / empty / malformed files."""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Place it in the same folder "
              f"as this program and try again.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: '{filename}' is empty.")
        return None
    except Exception as exc:
        print(f"Error: could not read '{filename}' ({exc}).")
        return None

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print("Error: missing column(s): " + ", ".join(missing))
        return None

    df["TotalSpent"] = pd.to_numeric(df["TotalSpent"], errors="coerce")
    df = df.dropna(subset=["TotalSpent"])
    if df.empty:
        print("Error: no valid customer records found.")
        return None
    return df


def spending_statistics(df):
    """Mean, median, highest and lowest spending."""
    mean = df["TotalSpent"].mean()
    median = df["TotalSpent"].median()
    top = df.loc[df["TotalSpent"].idxmax()]
    low = df.loc[df["TotalSpent"].idxmin()]

    print(f"Mean spend: Rs. {mean:.2f}")
    print(f"Median spend: Rs. {median:.2f}")
    print(f"Highest: {top['Name']} (Rs. {fmt(top['TotalSpent'])})")
    print(f"Lowest: {low['Name']} (Rs. {fmt(low['TotalSpent'])})")


def read_limit():
    """Ask for the limit; return a float, or None if invalid."""
    text = input("Enter spending limit: ").strip()
    try:
        limit = float(text)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None
    if limit != limit or limit in (float("inf"), float("-inf")):
        print("Invalid amount. Please enter a number.")
        return None
    if limit < 0:
        print("Amount must be 0 or more.")
        return None
    return limit


def high_value_customers(df):
    """List customers whose TotalSpent >= the limit entered by the user."""
    limit = read_limit()
    if limit is None:
        return

    result = df[df["TotalSpent"] >= limit]
    print(f"High-value customers (TotalSpent >= {fmt(limit)}): {len(result)}")
    for _, row in result.iterrows():
        print(f"{row['CustomerID']} | {row['Name']} | {row['City']} | "
              f"Rs. {fmt(row['TotalSpent'])}")


def city_summary(df):
    """City-wise total and average spending (highest total first)."""
    grouped = (df.groupby("City")["TotalSpent"]
                 .agg(["sum", "mean"])
                 .sort_values("sum", ascending=False))
    width = max(len(city) for city in grouped.index)
    for city, row in grouped.iterrows():
        print(f"{city.ljust(width)} : Total Rs. {fmt(row['sum'])} | "
              f"Average Rs. {row['mean']:.2f}")


def show_menu():
    print("\n===== Retail Customer Analyzer =====")
    print("1. Spending statistics")
    print("2. High-value customers")
    print("3. City-wise summary")
    print("4. Exit")


def main():
    df = load_data()
    if df is None:
        sys.exit(1)

    while True:
        show_menu()
        try:
            choice = input("Enter your choice (1-4): ").strip()
        except EOFError:
            break

        print()
        if choice == "1":
            spending_statistics(df)
        elif choice == "2":
            high_value_customers(df)
        elif choice == "3":
            city_summary(df)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
