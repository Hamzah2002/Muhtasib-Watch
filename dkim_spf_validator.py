import re
import logging

# Configure logging instead of print statements for better tracking
logging.basicConfig(level=logging.INFO)


def unfold_headers(email_headers):
    """
    Unfold headers by joining continuation lines.
    Continuation lines start with whitespace (space or tab).
    """
    unfolded_headers = ""
    for line in email_headers.splitlines():
        if line.startswith((' ', '\t')):
            # Continuation of the previous line
            unfolded_headers += line.strip()
        else:
            # New header
            unfolded_headers += "\n" + line.strip()

    return unfolded_headers.strip()


def filter_relevant_headers(email_headers):
    """
    Extract only the relevant headers for DKIM, SPF, and Authentication Results.
    """
    relevant_headers = []

    # Define a regex pattern for headers we care about
    patterns = [
        r'Received-SPF:.*',  # SPF result
        r'Authentication-Results:.*',  # Authentication results (SPF, DKIM, DMARC)
        r'DKIM-Signature:.*',  # DKIM signature
        r'Received:.*'  # Received headers (for debugging the path of the email)
    ]

    # For each line in the unfolded headers, check if it matches one of our patterns
    for line in email_headers.splitlines():
        for pattern in patterns:
            if re.match(pattern, line, re.IGNORECASE):
                relevant_headers.append(line)
                break

    logging.info(f"Filtered headers:\n{'\n'.join(relevant_headers)}")
    return "\n".join(relevant_headers)


def check_dkim(email_headers):
    """Extract DKIM-Signature and validate using the Authentication-Results header."""
    try:
        # Check for DKIM-Signature in the headers
        dkim_signature = re.findall(r'DKIM-Signature:.*', email_headers, re.IGNORECASE | re.DOTALL)
        if dkim_signature:
            for signature in dkim_signature:
                logging.info(f"DKIM Signature found: {signature}")

            # Check if DKIM passed in the Authentication-Results header
            dkim_auth_result = re.search(r'Authentication-Results:.*dkim=pass', email_headers, re.IGNORECASE)
            if dkim_auth_result:
                return "DKIM Signature appears valid based on Authentication-Results header"
            else:
                return "DKIM Signature is invalid based on Authentication-Results header"
        else:
            return "No DKIM-Signature found in the email headers."
    except Exception as e:
        logging.error(f"DKIM check failed: {str(e)}")
        return f"DKIM check failed: {str(e)}"


def check_spf(email_headers):
    """Extract SPF information and validate using the Received-SPF header."""
    try:
        # Extract SPF result from the 'Received-SPF' header
        spf_match = re.search(r'Received-SPF: (pass|fail|neutral|softfail).*?client-ip=([0-9.]+)', email_headers)
        if spf_match:
            spf_result = spf_match.group(1)
            sender_ip = spf_match.group(2)
            logging.info(f"SPF Info found: {spf_result}, Client IP: {sender_ip}")

            # Since Received-SPF indicates pass or fail, return that result
            return f"SPF Result: {spf_result}, Client IP: {sender_ip}"
        else:
            return "Could not extract SPF information for validation."
    except Exception as e:
        logging.error(f"SPF check failed: {str(e)}")
        return f"SPF check failed: {str(e)}"


def analyze_email(email_headers):
    """Run DKIM and SPF checks."""
    logging.info("\n--- Analyzing Email Headers ---")

    # First, unfold multi-line headers
    unfolded_headers = unfold_headers(email_headers)

    # Then filter out irrelevant headers
    filtered_headers = filter_relevant_headers(unfolded_headers)

    # DKIM Check
    dkim_result = check_dkim(filtered_headers)
    logging.info(f"DKIM Validation Result: {dkim_result}")

    # SPF Check
    spf_result = check_spf(filtered_headers)
    logging.info(f"SPF Validation Result: {spf_result}")


def get_email_headers():
    """Prompt the user to paste email headers and signal the end with 'END'."""
    print("Please copy and paste the relevant email headers below. Type 'END' when you are finished:\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


# Example usage:
if __name__ == "__main__":
    # Get email headers
    email_headers = get_email_headers()

    # Run the analysis
    analyze_email(email_headers)
