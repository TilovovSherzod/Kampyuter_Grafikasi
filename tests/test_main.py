import pytest


@pytest.mark.django_db
def test_root_returns_200(client):
    """Simple Django test: home page returns 200 and contains site title."""
    resp = client.get('/')
    assert resp.status_code == 200
    text = resp.content.decode('utf-8')
    assert 'Muhandislik kompyuter grafikasi' in text


def test_login_page_available(client):
    resp = client.get('/accounts/login/')
    # login page should be present (200) when auth URLs are enabled
    assert resp.status_code in (200, 302)
