import requests
from bs4 import BeautifulSoup

import pandas as pd

import csv

from stage2 import scrape_data_from_csv


def scrape_profile_links(url):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements with the class "info-section"
        info_sections = soup.find_all(class_="info-section")

        # Extract profile links from the info sections
        profile_links = []

        for info_section in info_sections:
            # Check if 'a' tag exists within the info_section
            link_tag = info_section.find('a')

            if link_tag and 'href' in link_tag.attrs:
                profile_links.append(link_tag['href'])

        return profile_links
    else:
        # Print an error message if the request was not successful
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None


def check_url_exist(base_url):
    page_number = 1
    all_doc_url = []

    count = 0
    while True:
        url_to_scrape = f'{base_url}?page={page_number}'

        doc_url = scrape_profile_links(url_to_scrape)

        if doc_url:
            print(f"Page {page_number} URL - Count: {len(doc_url)}")
            for url in doc_url:
                count += 1
                all_doc_url.append(url)

            page_number += 1
        else:
            break

    print(f"${base_url}:\t Count: func {len(all_doc_url)}: manual {count}")
    # for name in all_doctor_names:
    #     print(name)
    return count, base_url, all_doc_url


def read_excel_file(file_path, sheet_name='Sheet1'):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Convert the DataFrame to a list of dictionaries
        data_list = df.values.tolist()

        return data_list
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None


def main(output_excel_file_path='list_with_counts.csv'):
    # Specify the path to your Excel file
    excel_file_path = 'list.xlsx'
    # Specify the output file path

    work_url = []
    all_doc_url = []
    doc_cnt = 0
    count = 0
    nt_count = 0
    # Specify the sheet name (default is 'Sheet1')
    sheet_name = 'Sheet1'

    # Read the Excel file and create a list
    data_list = read_excel_file(excel_file_path, sheet_name)

    if data_list:
        for item in data_list:
            cnt, b_url, doc_url = check_url_exist(item[0])
            for d_url in doc_url:
                d_url = "https://www.practo.com" + d_url
                all_doc_url.append(d_url)

            if cnt:
                work_url.append(b_url)
                count += 1
                doc_cnt += cnt
            else:
                nt_count += 1
    print(f'Number of pages: work_url:{len(work_url)} cntr:{count}, Not Found: {nt_count}, Total: {count + nt_count}')
    print(len(data_list))
    print(f'Number of docs: doc_url: {len(all_doc_url)}, found: {doc_cnt}')

    with open(output_excel_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write data rows
        for url in all_doc_url:
            csv_writer.writerow([url])

    print(f'Data written to CSV file: {output_excel_file_path}')


if __name__ == "__main__":
    output_excel_file_path = 'list_with_counts.csv'
    main(output_excel_file_path)

    # Call the function to scrape data from the CSV file
    # scrape_data_from_csv(output_excel_file_path)
