import urllib.parse
from pathlib import Path
from typing import Iterable

try:
    import yaml
    from mdtemplate.table import TableTemplate
except ImportError:
    raise ImportError("Please install md-template: pip install md-template[full]")

IMPORT_BADGE = "[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url={0})"


yaml.SafeLoader.add_constructor("!input", lambda a, b: None)


class BlueprintTemplate(TableTemplate):
    table = "automation"
    files = "automation/*.yaml"
    columns = ("Blueprint", "Import")

    def handle_path(self, path: Path) -> Iterable[Iterable[str]]:
        with open(path) as file:
            blueprint = yaml.safe_load(file)["blueprint"]
        name = blueprint["name"]
        desc = blueprint["description"].split("\n")[0]

        yield [
            f"[**{name}**]({path.as_posix()})\n{desc}",
            IMPORT_BADGE.format(
                urllib.parse.quote(
                    f"https://raw.githubusercontent.com/{self.repository.owner}/{self.repository.name}/{self.repository.branch}/{path.as_posix()}"
                )
            ),
        ]


if __name__ == "__main__":
    BlueprintTemplate().parse_args().render()
