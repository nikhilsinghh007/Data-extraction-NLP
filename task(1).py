# Import necessary libraries
import requests  # For sending HTTP requests to the URLs
from bs4 import BeautifulSoup  # For parsing HTML content
import pandas as pd  # For reading Excel files and manipulating data

# upload the 'input.xlsx' file on the file explorer of whatever the platform you are running. 
# Define the path to the Excel file in the Replit environment
excel_file_path = './Input.xlsx'  # Adjust the path based on the actual location of the file

# Load the Excel file into a DataFrame
df = pd.read_excel(excel_file_path)

# Loop through each row in the DataFrame to process each URL and URL_ID
for index, row in df.iterrows():
    url = row['URL']  # Extract the URL from the current row; replace 'URL' with the actual column name if different
    url_id = row['URL_ID']  # Extract the URL_ID from the current row; replace 'URL_ID' with the actual column name if different

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the article title, typically found in the <h1> tag
        title = soup.find('h1').get_text()

        # Extract the main article content from the <div> with class 'td-post-content'
        article_body = soup.find('div', class_='td-post-content')

        if article_body:
            # Find all <p> tags within the article body (paragraphs)
            article_paragraphs = article_body.find_all('p')

            # Combine the paragraphs into a single string, filtering out paragraphs containing "contact"
            article_text = '\n'.join([para.get_text() for para in article_paragraphs if "contact" not in para.get_text().lower()])

            # Further filter the text to exclude paragraphs starting with "Summarized:"
            filtered_text = "\n".join([para for para in article_text.split('\n') if not para.strip().startswith("Summarized:")])

            # Save the extracted title and text into a text file named after the URL_ID
            with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
                file.write(title + '\n\n' + filtered_text)

            print(f"Article title and text have been saved to {url_id}.txt")
        else:
            print(f"Content not found for URL: {url}")
    except Exception as e:
        # Print any errors encountered during the process
        print(f"An error occurred with URL: {url} - {e}")
