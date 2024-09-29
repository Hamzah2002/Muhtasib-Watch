import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual VirusTotal API key
VIRUSTOTAL_API_KEY = 'd635a1884a18075799287f2dffa1edd09ba896a8a375745514a7dd0b12d2c8ec'


def expand_url(url):
    """
    Expand shortened URLs to their final destination by following redirects.
    """
    try:
        session = requests.Session()
        session.max_redirects = 10  # Allow up to 10 redirects
        response = session.head(url, allow_redirects=True)

        # Check if we detected any redirects
        if len(response.history) > 0:
            logging.info(f"Redirects found for URL '{url}': {[r.url for r in response.history]}")
            logging.info(f"Final URL after redirection: {response.url}")
        else:
            logging.info(f"No redirections found for URL '{url}'.")

        return response.url

    except requests.exceptions.TooManyRedirects:
        logging.warning(f"URL '{url}' has too many redirects and could be suspicious.")
        return None
    except Exception as e:
        logging.error(f"Error expanding URL {url}: {str(e)}")
        return None


def check_url_virustotal(url):
    """
    Check a single URL against VirusTotal's API to see if it's malicious.
    """
    api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey': VIRUSTOTAL_API_KEY, 'resource': url}

    try:
        logging.info(f"Checking URL: {url}")
        response = requests.get(api_url, params=params)

        # Check if the response was successful
        if response.status_code == 200:
            result = response.json()
            logging.info(f"VirusTotal Response: {result}")  # Log full response for debugging

            if result['response_code'] == 1:  # URL is present in VirusTotal's database
                if result['positives'] > 0:
                    return f"Malicious URL detected! {result['positives']} engines flagged this URL."
                else:
                    return "URL is clean according to VirusTotal."
            else:
                return "URL not found in VirusTotal's database."
        else:
            return f"Failed to retrieve data from VirusTotal. Status code: {response.status_code}, Message: {response.text}"

    except ValueError as ve:
        logging.error(f"Invalid JSON response: {str(ve)}")
        return f"Error parsing response from VirusTotal: {str(ve)}"
    except Exception as e:
        logging.error(f"Error checking URL {url}: {str(e)}")
        return f"Error checking URL: {str(e)}"


# Example usage:
if __name__ == "__main__":
    url = input("Enter the URL to check: ").strip()

    # Step 1: Expand shortened URLs
    expanded_url = expand_url(url)
    if expanded_url:
        logging.info(f"Checking the final URL: {expanded_url}")
        # Step 2: Check the final URL against VirusTotal
        result = check_url_virustotal(expanded_url)
        print(result)
    else:
        print("Could not resolve the URL or it has suspicious redirections.")
