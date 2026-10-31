import ipaddress
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

MAX_BYTES = 5_000_000

def _is_safe_url(url:str)->bool:
    """ only http/https URLs in public internet"""
    parsed =  urlparse(url)
    if parsed.scheme not in ("https","http") or not parsed.hostname:
        return False 
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    except (socket.gaierror, ValueError):
        return False
    return not(ip.is_private or ip.is_loopback or ip.is_link_local)

def extract_text_url(url:str)->str:
    url=url.strip()
    if not _is_safe_url(url):
        raise ValueError("That doesn't look like a valid pyblic web address, try another method (paste text) or (upload the document)")
    resp = requests.get(
        url, 
        timeout= 10,
        headers= {"User-Agent":"Mozilla/5.0 (Fairles project)"}

    )    
    resp.raise_for_status()
    if len(resp.content)> MAX_BYTES:
        raise ValueError("the page is too large, try another page of the same content.")


    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script","style","nav","footer","header","noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    text= "\n".join(line for line in lines if line)

    if len(text)<500:
        raise ValueError("Couldn't read enough text from this page, please try to paste the text instead.")
 
    return text


if __name__ == "__main__":
    print(extract_text_url("https://code.claude.com/docs/en/legal-and-compliance")[:300])