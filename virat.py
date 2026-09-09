import json
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

API_URL = "https://commons.wikimedia.org/w/api.php"
IMAGE_PATH = Path(__file__).with_name("virat_kohli.jpg")

def download_virat_kohli_photo() -> Path:
	"""Find a Wikimedia Commons image and save it beside this script."""
	query = urllib.parse.urlencode(
		{
			"action": "query",
			"format": "json",
			"generator": "search",
			"gsrsearch": "Virat Kohli",
			"gsrnamespace": 6,
			"gsrlimit": 10,
			"prop": "imageinfo",
			"iiprop": "url|mime",
		}
	)
	request = urllib.request.Request(
		f"{API_URL}?{query}",
		headers={"User-Agent": "virat-photo-example/1.0"},
	)

	with urllib.request.urlopen(request, timeout=20) as response:
		results = json.load(response)

	pages = results.get("query", {}).get("pages", {})
	image_url = next(
		(
			page["imageinfo"][0]["url"]
			for page in pages.values()
			if page.get("imageinfo")
			and page["imageinfo"][0].get("mime", "").startswith("image/")
		),
		None,
	)
	if image_url is None:
		raise RuntimeError("No suitable Virat Kohli image was found.")

	image_request = urllib.request.Request(
		image_url,
		headers={"User-Agent": "virat-photo-example/1.0"},
	)
	with urllib.request.urlopen(image_request, timeout=20) as response:
		IMAGE_PATH.write_bytes(response.read())
	return IMAGE_PATH

if __name__ == "__main__":
	photo_path = download_virat_kohli_photo()
	print(f"Downloaded Virat Kohli photo to: {photo_path}")
	webbrowser.open(photo_path.as_uri())
