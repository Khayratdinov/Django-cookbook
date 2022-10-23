import re

# ============================================================================ #
from django import template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

# ============================================================================ #
from datetime import datetime


register = template.Library()

""" FILTERS """
DAYS_PER_YEAR = 365
DAYS_PER_MONTH = 30
DAYS_PER_WEEK = 7


@register.filter(is_safe=True)
def date_since(specific_date):
    today = timezone.now().date()
    if isinstance(specific_date, datetime):
        specific_date = specific_date.date()
    diff = today - specific_date
    diff_years = int(diff.days / DAYS_PER_YEAR)
    diff_months = int(diff.days / DAYS_PER_MONTH)
    diff_weeks = int(diff.days / DAYS_PER_WEEK)
    diff_map = [
        (
            "year",
            "years",
            diff_years,
        ),
        (
            "month",
            "months",
            diff_months,
        ),
        (
            "week",
            "weeks",
            diff_weeks,
        ),
        (
            "day",
            "days",
            diff.days,
        ),
    ]
    for parts in diff_map:
        (
            interval,
            intervals,
            count,
        ) = parts
        if count > 1:
            return _(f"{count} {intervals} ago")
        elif count == 1:
            return _("yesterday") if interval == "day" else _(f"last {interval}")
    if diff.days == 0:
        return _("today")
    else:
        # Date is in the future; return formatted date.
        return f"{specific_date:%B %d, %Y}"


MEDIA_CLOSED_TAGS = "|".join(["figure", "object", "video", "audio", "iframe"])
MEDIA_SINGLE_TAGS = "|".join(["img", "embed"])
MEDIA_TAGS_REGEX = re.compile(
    r"<(?P<tag>"
    + MEDIA_CLOSED_TAGS
    + ")[\S\s]+?</(?P=tag)>|"
    + r"<("
    + MEDIA_SINGLE_TAGS
    + ")[^>]+>",
    re.MULTILINE,
)


@register.filter
def first_media(content):
    """
    Returns the chunk of media-related markup from the html content
    """
    tag_match = MEDIA_TAGS_REGEX.search(content)
    media_tag = ""
    if tag_match:
        media_tag = tag_match.group()
    return mark_safe(media_tag)
