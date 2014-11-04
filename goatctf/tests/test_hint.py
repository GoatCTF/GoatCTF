import pytest
from core.models import Challenge, Hint


@pytest.fixture
def challenge():
    c = Challenge(name="Get Crunk", category='be', points=100)
    c.save()
    return c


@pytest.mark.django_db
def test_auto_populate_publish_date(challenge):
    hint = Hint(challenge=challenge, content_markdown='')
    hint.save()
    assert hint.publish_date is not None


@pytest.mark.django_db
def test_markdown_compiles_on_save(challenge):
    hint = Hint(challenge=challenge)
    hint.content_markdown = """# Title
## Subtitle

Paragraph

Another paragraph
"""
    hint.save()
    assert hint.content_html == (
        "<h1>Title</h1>\n<h2>Subtitle</h2>\n<p>Paragraph</p>\n<p>Another "
        "paragraph</p>")
