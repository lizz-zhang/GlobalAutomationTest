from urllib.parse import urlparse


def get_root_domain(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split(".")
    if len(domain_parts) > 2:
        return "." + ".".join(domain_parts[-2:])
    return parsed_url.netloc
