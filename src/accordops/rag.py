from pathlib import Path


def chunker(path: Path):
    sections = []
    section = []
    with path.open() as f:
        for line in f:
            if line.startswith("##"):
                if section:
                    sections.append(section)
                section = [line]
            else:
                section.append(line)
    if section:
        sections.append(section)

    return ["\n".join(section).strip() for section in sections]
