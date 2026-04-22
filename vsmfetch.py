import tomllib
import ads
import pandas


TOKEN_CONFIG_FILENAME = "token.toml"
CONFIG_FILENAME = "config.toml"


def read_toml(filename: str) -> dict:
    with open(filename, "rb") as file:
        return tomllib.load(file)
    

def compile(papers: list) -> dict:
    compilation = {
        "title": [],
        "abstract": [],
        "bibcode": [],
        "author": [],
        "year": [],
        "keyword": [],
        "ads_url": [],
        "url": [],
    }

    for paper in papers:
        compilation["title"].append(";;".join(paper.title))
        compilation["abstract"].append(paper.abstract)
        compilation["bibcode"].append(paper.bibcode)
        compilation["author"].append(";;".join(paper.author))
        compilation["year"].append(paper.year)
        compilation["keyword"].append(";;".join(paper.keyword) if isinstance(paper.keyword, list) else "-")
        compilation["ads_url"].append(f"https://ui.adsabs.harvard.edu/abs/{paper.bibcode}/abstract")
        compilation["url"].append(f"https://ui.adsabs.harvard.edu/link_gateway/{paper.bibcode}/{paper.esources[0]}" if isinstance(paper.esources, list) else "-")

    return compilation


def main():
    token = read_toml(TOKEN_CONFIG_FILENAME)["token"]
    ads.config.token = token

    config = read_toml(CONFIG_FILENAME)
    keywords = config["keywords"]
    rows = config["rows"]

    query = f'abs:("{ '" OR "'.join(keywords) }")'

    papers = list(ads.SearchQuery(
        q=query,
        fl=['title', 'abstract', 'bibcode', 'author', 'year', 'keyword', 'esources'],
        rows=rows
    ))

    output_filename = config["output"]

    pandas.DataFrame(compile(papers)).to_excel(output_filename, index=False)
