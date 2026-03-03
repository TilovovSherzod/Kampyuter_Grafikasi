from django import template

register = template.Library()


@register.simple_tag
def seq(start, end):
    """Return an iterable range from start (inclusive) to end (exclusive).

    Usage in template:
      {% load range_tags %}
      {% seq 1 16 as nums %}
      {% for i in nums %} ... {% endfor %}
    """
    try:
        s = int(start)
        e = int(end)
    except Exception:
        return []
    # mimic Python range(start, end)
    return range(s, e)
