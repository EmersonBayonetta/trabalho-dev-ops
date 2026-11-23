from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "index.html"


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"ID duplicado: #{element_id}")
            self.ids.add(element_id)

        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value is not None:
                self.references.append((tag, attribute, value))


def valid_email(value):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value))


def check_reference(parser, tag, attribute, value):
    parsed = urlsplit(value)

    if parsed.scheme in ("http", "https"):
        if not parsed.hostname or parsed.username or parsed.password:
            parser.errors.append(f"URL externa inválida em <{tag}> {attribute}: {value}")
            return
        try:
            parsed.port
        except ValueError:
            parser.errors.append(f"Porta inválida em <{tag}> {attribute}: {value}")
        return

    if parsed.scheme == "mailto":
        if not valid_email(parsed.path):
            parser.errors.append(f"Endereço de e-mail inválido em <{tag}>: {value}")
        return

    if parsed.scheme or parsed.netloc:
        parser.errors.append(f"Protocolo não suportado em <{tag}> {attribute}: {value}")
        return

    if parsed.path:
        local_path = (ROOT / unquote(parsed.path)).resolve()
        if not local_path.is_relative_to(ROOT) or not local_path.is_file():
            parser.errors.append(f"Arquivo local inexistente em <{tag}> {attribute}: {value}")
            return

    if parsed.fragment and unquote(parsed.fragment) not in parser.ids:
        parser.errors.append(f"Âncora inexistente em <{tag}>: #{unquote(parsed.fragment)}")


def main():
    if not HTML_FILE.is_file():
        print("Erro: index.html não existe na raiz do projeto.", file=sys.stderr)
        return 1

    parser = ReferenceParser()
    parser.feed(HTML_FILE.read_text(encoding="utf-8"))
    for tag, attribute, value in parser.references:
        check_reference(parser, tag, attribute, value)

    if parser.errors:
        for error in parser.errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1

    print(f"Referências válidas: {len(parser.references)} links e imagens.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
