# Jidouteki

Jidouteki ("自動的", "automatic") is a website-independed manga sources and data extractor.

It uses python parsers to describe website structures and provides many convenience methods to get parsers writen quickly and accurately.

## Example

Given a `google-drive.py` file 

```python
import jidouteki

class GDrive(WebsiteParser):
    def meta(self):
        return jidouteki.Metadata(
            base = 'https://drive.google.com/',
            key = 'google-drive',
            display_name = 'Google drive'
        )

    @jidouteki.match
    def match(self):
        return (
            r"https://drive\.google\.com/drive/folders/(?P<folderId>.*?)(?:[/?].*|)$",
        )
  
    @jidouteki.images
    def images(self, folderId):
        d = self.utils.fetch(f"/drive/folders/{folderId}")
        d = d.css("c-wiz > div[data-id]")
        
        images = []
        for el in d:
            data_id = el["data-id"]
            images.append(f"https://lh3.googleusercontent.com/d/{data_id}")
        return images
```

The following code

```python
from jidouteki import Jidouteki

jdtk = Jidouteki(
    proxy="https://your-cors-proxy/"
)

gdrive = jdtk.load_provider("google-drive.py")

images = gdrive.images(<folderId>) 
print(images)
```

Will print all the urls of the images contained the google-drive `folderId` folder.

The parsers are publicily hosted over on [ridamoe/parsers](https://github.com/ridamoe/parsers).
Contributions are welcome!

## TODO

- Document api
