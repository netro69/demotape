# Created-by: architect | Date: 2026-09-22
from django import template

register = template.Library()


@register.inclusion_tag('core/verification_badge.html')
def verification_badge(link):
    """Render verification badge for a Link object."""
    level = link.verification_level
    if level == 4:
        symbol = '✓'
        css_class = 'badge-verified'
        label = 'Verified — admin confirmed'
    elif level == 3:
        symbol = '◐'
        css_class = 'badge-pending'
        label = 'Auto-verified — pending admin review'
    elif level == 2:
        symbol = '◐'
        css_class = 'badge-pending'
        label = 'Cross-referenced'
    elif level == 1:
        symbol = '◐'
        css_class = 'badge-pending'
        label = 'Discovered — not yet verified'
    else:
        symbol = '✗'
        css_class = 'badge-flagged'
        label = 'Flagged — needs review'
    
    return {
        'symbol': symbol,
        'css_class': css_class,
        'label': label,
        'level': level,
        'link': link,
    }
