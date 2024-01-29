import requests
from bs4 import BeautifulSoup
import re
import csv


def scrape_doctor_info(url, city):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract doctor name
        doctor_name_element = soup.find('h1', {'data-qa-id': 'doctor-name',
                                               'class': 'c-profile__title u-bold u-d-inlineblock'})
        doctor_name = doctor_name_element.text.strip() if doctor_name_element else None

        # Extract doctor qualifications
        qualifications_element = soup.find('p', {'class': 'c-profile__details', 'data-qa-id': 'doctor-qualifications'})
        qualifications = qualifications_element.text.strip() if qualifications_element else None

        # Extract doctor specializations
        specializations_element = soup.find('div',
                                            {'class': 'c-profile__details', 'data-qa-id': 'doctor-specializations'})
        specializations = specializations_element.text.strip().replace('\xa0', ' ') if specializations_element else None
        match = re.search(r'(\D+)(\d.*)', specializations)

        specializations = None
        experience = None
        if match:
            specializations = match.group(1).strip()
            experience = match.group(2).strip()
        # Extract clinic address
        clinic_address_element = soup.find('p', {'class': 'c-profile--clinic__address', 'data-qa-id': 'clinic-address'})
        clinic_address = clinic_address_element.text.strip() if clinic_address_element else None

        # Extract consultation fee
        consultation_fee_element = soup.find('span', {'data-qa-id': 'consultation_fee'})
        consultation_fee = consultation_fee_element.text.strip() if consultation_fee_element else None
        consultation_fee = consultation_fee if isinstance(consultation_fee,(str,bytes)) else '0'
        if not  consultation_fee =='0':
            match = re.search(r'(\D+)(\d.*)', consultation_fee)
            consultation_fee = match.group(2).strip() 
        # Add city to the extracted information
        doctor_info_list = [doctor_name, qualifications, specializations, experience, clinic_address, city.title(),
                            consultation_fee]

        return doctor_info_list
    else:
        # Print an error message if the request was not successful
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None


def scrapeDoc(url):
    start_string = 'https://www.practo.com/'
    end_string = '/doctor'

    # Use regular expression to extract the substring between the two strings
    pattern = re.compile(re.escape(start_string) + '(.*?)' + re.escape(end_string))
    match = pattern.search(url)
    city = match.group(1) if match else None

    doctor_info = scrape_doctor_info(url, city)

    if doctor_info:
        # print("Doctor Information:")
        print(doctor_info)
        # for info in doctor_info:
        #     print(info)
        return doctor_info
    return None


def read_csv_file(file_path):
    try:
        # Read the CSV file into a list of lists
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            data_list = [row for row in csv_reader]

        return data_list
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def scrape_data_from_csv(csv_file_path):
    # Read CSV file into a list of lists
    data_list = read_csv_file(csv_file_path)
    scraped_data_list = []
    if data_list:
        # Iterate over each row in the CSV file
        for row in data_list:
            if len(row) > 0:  # Check if the row is not empty
                url = row[0]  # Assuming the URL is in the first column of the CSV

                # Call your scraping function with the URL
                dat = scrapeDoc(url)
                scraped_data_list.append(dat)
    # Write the scraped data to a new CSV file
    with open('scraped_doc_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        # Write header
        csv_writer.writerow(['Doctor Name', 'Qualifications', 'Specializations', 'Experience', 'Clinic Address', 'City',
                             'Consultation Fee'])

        # Write scraped data rows
        for dat in scraped_data_list:
            if dat is not None:
                dat = [value.strip('"') if value is not None else "" for value in dat]
                csv_writer.writerow(dat)


# Your scraping functions...

if __name__ == "__main__":
    # Specify the path to your CSV file
    csv_file_path = 'list_with_counts.csv'

    # Call the function to scrape data from the CSV file
    scrape_data_from_csv(csv_file_path)
