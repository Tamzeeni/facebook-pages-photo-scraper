import csv
import requests
import os

# Define the directory where images will be saved
download_directory = "downloaded_photos"

# Create the directory if it does not exist
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Function to download a photo from a given URL
def download_image(photo_url, filename):
    try:
        # Send a request to download the image
        response = requests.get(photo_url, stream=True)
        if response.status_code == 200:
            # Save the image content to a file
            with open(filename, 'wb') as out_file:
                out_file.write(response.content)
            print(f"Successfully downloaded: {filename}")
        else:
            print(f"Failed to download {filename} - HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Read the CSV file and download each image
csv_file = "photo_data.csv"

try:
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            photo_url = row['Photo URL']  # Assuming this is the column name for the image URL
            if photo_url:
                # Generate the filename based on the image URL
                image_name = os.path.join(download_directory, os.path.basename(photo_url))
                download_image(photo_url, image_name)
except FileNotFoundError:
    print(f"The file '{csv_file}' was not found.")
except Exception as e:
    print(f"An error occurred while processing the CSV file: {e}")

print("Download process complete.")

