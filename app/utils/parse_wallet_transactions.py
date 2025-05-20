import csv
from decimal import Decimal

def parse_wallet_transactions(input_csv, output_csv):
    """
    Parses raw wallet transactions CSV and outputs IRS-friendly tax report CSV.

    Expected input CSV columns (example): 
    Date,Type,Asset,Quantity,USD_Value,From,To,Tx_Hash

    Output CSV columns:
    Date,Transaction Type,Asset,Quantity,Price per Unit (USD),Proceeds (USD),Cost Basis (USD),Gain/Loss (USD),Notes
    """
    transactions = []

    with open(input_csv, newline='') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            date = row['Date']
            tx_type_raw = row['Type'].lower()
            asset = row['Asset']
            quantity = Decimal(row['Quantity'])
            usd_value = Decimal(row['USD_Value'])

            # Basic price per unit calculation
            price_per_unit = usd_value / quantity if quantity != 0 else Decimal('0')

            # Map raw types to IRS-friendly types
            if tx_type_raw in ('buy', 'deposit'):
                tx_type = 'Buy'
                proceeds = Decimal('0')
                cost_basis = usd_value
                gain_loss = Decimal('0')
                notes = ''
            elif tx_type_raw in ('sell', 'withdraw'):
                tx_type = 'Sale'
                proceeds = usd_value
                cost_basis = Decimal('UNKNOWN')  # Placeholder; user must input or calculate cost basis
                gain_loss = Decimal('UNKNOWN')   # Placeholder
                notes = 'Cost basis/gain-loss needs calculation'
            elif tx_type_raw == 'trade':
                tx_type = 'Trade'
                proceeds = usd_value
                cost_basis = Decimal('UNKNOWN')
                gain_loss = Decimal('UNKNOWN')
                notes = 'Cost basis/gain-loss needs calculation'
            elif tx_type_raw == 'loss_claim':
                tx_type = 'Loss Claim'
                proceeds = Decimal('0')
                cost_basis = Decimal('0')
                gain_loss = -usd_value
                notes = 'Reported loss'
            else:
                tx_type = tx_type_raw.capitalize()
                proceeds = usd_value
                cost_basis = Decimal('UNKNOWN')
                gain_loss = Decimal('UNKNOWN')
                notes = 'Check transaction type'

            transactions.append({
                'Date': date,
                'Transaction Type': tx_type,
                'Asset': asset,
                'Quantity': str(quantity),
                'Price per Unit (USD)': f"{price_per_unit:.2f}",
                'Proceeds (USD)': str(proceeds),
                'Cost Basis (USD)': str(cost_basis),
                'Gain/Loss (USD)': str(gain_loss),
                'Notes': notes,
            })

    with open(output_csv, 'w', newline='') as outfile:
        fieldnames = ['Date','Transaction Type','Asset','Quantity','Price per Unit (USD)',
                      'Proceeds (USD)','Cost Basis (USD)','Gain/Loss (USD)','Notes']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for tx in transactions:
            writer.writerow(tx)

if __name__ == "__main__":
    # This is an example of how to use the function.
    # You'll need to create a 'wallet_raw.csv' file in the same directory
    # or provide the correct path to your input CSV file.
    # The output will be saved to 'crypto_tax_report.csv'.
    # It's recommended to call this function from another script 
    # or integrate it into your application's workflow.
    # For example:
    # from app.utils.parse_wallet_transactions import parse_wallet_transactions
    # parse_wallet_transactions('path/to/your/wallet_raw.csv', 'path/to/your/crypto_tax_report.csv')
    
    # Example usage (assuming 'wallet_raw.csv' exists in the same directory as this script):
    # try:
    #     parse_wallet_transactions('wallet_raw.csv', 'crypto_tax_report.csv')
    #     print("Successfully parsed transactions and generated 'crypto_tax_report.csv'")
    # except FileNotFoundError:
    #     print("Error: 'wallet_raw.csv' not found. Please create it or provide the correct path.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    pass # The __main__ block is typically for testing or direct execution, 
         # which might not be the primary use case when integrated into a larger app.
         # Kept the original logic but commented out direct execution to prevent errors
         # if 'wallet_raw.csv' is not present during automated runs or tests.
         # The user can uncomment and modify paths if they wish to run this script directly.
