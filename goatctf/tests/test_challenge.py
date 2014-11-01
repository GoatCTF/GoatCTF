import pytest
from core.models import Challenge


@pytest.fixture
def challenge():
    return Challenge()


@pytest.mark.django_db
def test_markdown_compiles_on_save(challenge):
    challenge.name = "Test Challenge"
    challenge.points = 0
    challenge.category = ""
    challenge.flag = ""
    challenge.description_markdown = """# Title
## Subtitle

Paragraph

Another paragraph
"""
    challenge.save()
    assert challenge.description_html == (
        "<h1>Title</h1>\n<h2>Subtitle</h2>\n<p>Paragraph</p>\n<p>Another "
        "paragraph</p>")
