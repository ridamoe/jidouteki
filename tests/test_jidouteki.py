import pytest
from jidouteki import Jidouteki, Config
from pathlib import Path
from urllib.parse import urlparse
import requests

config_path = Path("/mnt/data/Linux/Projects/ridamoe/Jidouteki2/configs")

jdtk = Jidouteki(
    proxy = "http://rida.moe/api/proxy"
)

configs = jdtk.load_directory(config_path)

@pytest.fixture()
def config(config_key):
    for config in configs:
        if config.meta.key == config_key:
            return config
    
@pytest.mark.parametrize('config_key,input,expected', [
    (
        'rawkuma', 
        "https://google.com", 
        None
    ),
    (
        "rawkuma", 
        "https://rawkuma.com/100-man-no-inochi-no-ue-ni-ore-wa-tatte-iru-chapter-94/", 
        {"series": "100-man-no-inochi-no-ue-ni-ore-wa-tatte-iru","chapter": "94"},
    ),
        (
        "rawkuma", 
        "https://rawkuma.com/manga/100-man-no-inochi-no-ue-ni-ore-wa-tatte-iru/", 
        {"series": "100-man-no-inochi-no-ue-ni-ore-wa-tatte-iru"},
    ),
    (
        "retsuorg",
        "https://retsu.org/manga/ao-no-hako/ch-130/",
        {"series": "ao-no-hako", "chapter": "130"}
    ),
    (
        "retsuorg",
        "https://retsu.org/manga/haruka-reset/chapter-71/",
        {"series": "haruka-reset", "chapter": "71"}
    ),
    (
        "google-drive",
        "https://drive.google.com/drive/folders/1VgP78U0tZtyfz9zVnXbghyFooAZ-UuxD?usp=drive_link",
        {"folderId": "1VgP78U0tZtyfz9zVnXbghyFooAZ-UuxD"}
    )
])
def test_match(config: Config, input, expected):
    value = config.match(input)
    assert value == expected, f"Expected {expected} got {value}"

@pytest.mark.parametrize("config_key,input", [
    (
        "manganato",
        {"series": "jv986530"} # on manganato.com
    ),
    (
        "manganato",
        {"series": "lb988758"} # on chapmanganato.to
    ),
    (
        "mangadex",
        {"series": "e1b08943-1195-4eab-85a4-a7bfc0766eed"}
    )
])
def test_has_chapters(config: Config, input):
    value = config.series.chapters(**input)
    assert len(value) > 0, f"No chapters for {input}"

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
import filetype
def is_image_url(url):
    try:
        resp = requests.get(url)
        if resp.ok: 
            if resp.headers['Content-Type'].startswith('image/'): return True
            return filetype.is_image(resp.content)
        else: return False
    except requests.exceptions.RequestException as e:
        return False

@pytest.mark.parametrize("config_key,input", [
    (
        "google-drive",
        {"folderId": "1VgP78U0tZtyfz9zVnXbghyFooAZ-UuxD"}
    ),
    (
        "retsuorg",
        { "series": "haruka-reset", "chapter": 71}
    ),
    (
        "retsuorg",
        { "series": "haruka-reset", "chapter": "71"}
    ),
    (
        "rawkuma",
        {"series": "100-man-no-inochi-no-ue-ni-ore-wa-tatte-iru", "chapter": "31"}
    ),
    (
        "manganato",
        { "series": "pn993048", "chapter": "1"}
    ),
    (
        "mangadex",
        {"chapter": "578eb707-acf3-4fcd-a383-054d116cdf00"}
    )
])
def test_images(config: Config, input):
    value = config.images(**input)
    assert len(value) > 0, f"No pages for {input}"
    
    for url in value:
        assert is_valid_url(url), f"{url} is not a valid url"
        # assert is_image_url(url), f"{url} is not an image"
        

@pytest.mark.parametrize("config_key,input", [
    (
        "mangadex",
        {"series": "e1b08943-1195-4eab-85a4-a7bfc0766eed"}
    )
])
def test_cover(config: Config, input):
    value = config.series.cover(**input)
    assert value, f"No cover for {input}"
    assert is_valid_url(value), f"{value} is not a valid url"
    # assert is_image_url(value), f"{value} is not an image"
