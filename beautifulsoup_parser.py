from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urlparse


def extract_statistics_score(soup: BeautifulSoup) -> float:

    text = soup.get_text(" ", strip=True).lower()
    sentences = re.split(r'[.!?]', text) #get all the sentences
    
    numbers = re.findall(r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?%?\b", text) #detect any numbers
    num_ratio = len(numbers) / max(len(text.split()), 1)
    
    table_tags = len(soup.find_all(["table", "figure", "figcaption"]))
    img_charts = len([img for img in soup.find_all("img") 
                      if any(x in (img.get("alt","")+img.get("src","")).lower() for x in ["chart", "graph", "data"])])
    
    stat_words = ["percent", "data", "average", "increase", "decrease", "survey", "figure"]
    stat_kw_count = sum(text.count(w) for w in stat_words)
    
    raw_score = num_ratio*50 + table_tags*2 + img_charts*3 + stat_kw_count*0.1
    score = min(1.0, raw_score / 10)
    return score


def extract_quotation_score(soup: BeautifulSoup) -> float:

    text = soup.get_text(" ", strip=True)
    
    # (1) HTML tags for quotes
    q_tags = len(soup.find_all(["q", "blockquote"]))
    
    # (2) Text-based quotes (within quotation marks)
    quoted_phrases = re.findall(r'["“”][^"“”]{5,200}["“”]', text)
    
    # (3) Attribution keywords
    verbs = ["said", "stated", "reported", "claimed", "noted"]
    verb_count = sum(text.lower().count(v) for v in verbs)
    
    raw_score = q_tags*2 + len(quoted_phrases)*0.5 + verb_count*0.1
    score = min(1.0, raw_score / 8)
    
    return round(score, 3)


def extract_cite_sources_score(soup: BeautifulSoup, domain) -> float:

    text = soup.get_text(" ", strip=True).lower()
    
    
    links = soup.find_all("a", href=True)
    external_links = [a for a in links if urlparse(a["href"]).netloc not in ("", domain)]
    
    citation_kw = sum(text.count(w) for w in ["reference", "references", "source", "sources", "bibliography", "citation"])
    
    sup_tags = len(soup.find_all("sup"))
    
    raw_score = len(external_links)*0.2 + citation_kw*0.5 + sup_tags*0.2
    score = min(1.0, raw_score / 8)
    
    return round(score, 3)


def analyse_site(url: str) -> dict:

    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    domain = urlparse(url).netloc

    statistics_score = extract_statistics_score(soup)
    quotation_score = extract_quotation_score(soup)
    cite_sources_score = extract_cite_sources_score(soup, domain)

    return {
        "statistics_score": statistics_score,
        "quotation_score": quotation_score,
        "cite_sources_score": cite_sources_score
    }


if __name__ == "__main__":
    url = "https://www.aljazeera.com/news/2021/11/1/modi-india-to-hit-net-zero-climate-target-by-2070"
    print(analyse_site(url))