class DocGenerator:

    def __init__(self, template: str = ""):
        self.template = template

    def generate(self, data: dict) -> str:
        doc = self.template
        for key, value in data.items():
            doc = doc.replace(f"{{{key}}}", str(value))
        return doc