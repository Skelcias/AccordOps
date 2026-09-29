from pathlib import Path


def chunker(path: Path):
    sections = []
    category = None
    with path.open() as f:
        for line in f:
            line = line.strip()

            if line.startswith("##"):
                category = line.removeprefix("## ").strip().lower()
                continue
            if line.startswith("# ") or not line:
                continue
            if category is not None:
                sections.append(
                    {
                        "category": category,
                        "content": f"{category} -- {line}",
                    }
                )

    return sections
