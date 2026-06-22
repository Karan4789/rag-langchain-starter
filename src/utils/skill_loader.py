# src/utils/skill_loader.py

SKILLS_DIR = "src/skills"

def load_skill(document_type: str) -> str:

    skill_map = {
        "spreadsheet": "spreadsheet_skill.md",
        "resume": "resume_skill.md",
        "book": "book_skill.md",
        
    }

    skill_file = skill_map.get(
        document_type,
        "default_skill.md"
    )

    skill_path = skill_map.get(
        document_type,
        "default_skill.md"
    )

    try:
        with open(
        f"src/skills/{skill_file}",
        "r",
        encoding="utf-8"
    ) as f:
            return f.read()

    except Exception:
        return ""