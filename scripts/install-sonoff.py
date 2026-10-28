#!/usr/bin/env python3
"""Instala SonoffLAN v3.13.2 sin HACS; no modifica una instalación existente."""
import io
import json
from pathlib import Path, PurePosixPath
import tempfile
import urllib.request
import zipfile

VERSION = "v3.13.2"
URL = f"https://api.github.com/repos/AlexxIT/SonoffLAN/zipball/{VERSION}"
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/homeassistant/custom_components/sonoff"


def main():
    if TARGET.exists():
        raise SystemExit(f"Ya existe {TARGET}; no se sobrescribe.")
    request = urllib.request.Request(URL, headers={"User-Agent": "DomotiK-local-setup"})
    with urllib.request.urlopen(request, timeout=60) as response:
        archive = response.read()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=TARGET.parent) as temporary:
        staging = Path(temporary) / "sonoff"
        with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
            for member in zipped.infolist():
                parts = PurePosixPath(member.filename).parts
                if len(parts) < 4 or parts[1:3] != ("custom_components", "sonoff"):
                    continue
                relative = PurePosixPath(*parts[3:])
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError("Ruta inválida en el archivo descargado")
                if member.is_dir():
                    continue
                destination = staging.joinpath(*relative.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(zipped.read(member))
        manifest = json.loads((staging / "manifest.json").read_text())
        if manifest.get("domain") != "sonoff" or manifest.get("version") != VERSION.lstrip("v"):
            raise ValueError("La integración descargada no corresponde a la versión esperada")
        staging.rename(TARGET)
    print(f"SonoffLAN {VERSION} instalado en {TARGET}")


if __name__ == "__main__":
    main()
