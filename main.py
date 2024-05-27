import requests
from bs4 import BeautifulSoup
import pandas as pd
from cryptography.fernet import Fernet
import subprocess


# Step 1: Web Scraping
def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting insurance companies and settlement percentages
        companies = soup.find_all("h3", class_="heading5")
        percentages = soup.find_all("p", class_="normal")

        data = [("Company", "Settlement Percentage")]

        for company, percentage in zip(companies, percentages):
            company_name = company.text.strip()
            settlement_percentage = percentage.text.strip()
            data.append((company_name, settlement_percentage))

        return data
    else:
        print("Failed to retrieve data from the website.")
        return None


# Step 2: Data Organization
def organize_data(data):
    # Organize scraped data into a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    return df


# Step 3: CSV File Creation
def create_csv(df, filename):
    df.to_csv(filename, index=False)
    print("CSV file created successfully.")


# Step 4: Encryption
def encrypt_file(filename, key):
    with open(filename, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(filename, 'wb') as f:
        f.write(encrypted_data)

    print("File encrypted successfully.")


# Step 5: Command-line Encryption
def command_line_encrypt(filename, encrypted_filename, key_file):
    subprocess.run([
        'openssl', 'enc', '-aes-256-cbc', '-salt', '-in', filename, '-out',
        encrypted_filename, '-pass', 'file:' + key_file
    ])
    print("File encrypted via command line.")


# Main Function
def main():
    # URL of the designated website
    url = "https://economictimes.indiatimes.com/wealth/insure/life-insurance/latest-life-insurance-claim-settlement-ratio-of-insurance-companies-in-india/articleshow/97366610.cms"
    # Filename for the CSV file
    csv_filename = "death_claims.csv"
    # Filename for the encrypted CSV file
    encrypted_filename = "encrypted_death_claims.csv"
    # Filename for the encryption key
    key_file = "encryption_key.txt"

    # Scrape data
    data = scrape_data(url)
    if data:
        # Organize data
        df = organize_data(data)
        # Create CSV file
        create_csv(df, csv_filename)
        # Generate encryption key
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        # Encrypt CSV file
        encrypt_file(csv_filename, key)
        # Command-line encryption
        command_line_encrypt(csv_filename, encrypted_filename, key_file)


if __name__ == "__main__":
    main()
