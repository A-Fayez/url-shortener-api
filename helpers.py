import uuid
import re


def generate_slug(length=6):
    """Generates a random char sequence for the slug"""

    return str(uuid.uuid4())[:length]


def valid_schema(ios_primary, ios_fallback, android_primary, android_fallback, web):
    """A helper function that checks some required args are presend
        and checks if the fields are valid urls"""

    if (
        not ios_primary
        and not ios_fallback
        and not android_primary
        and not android_fallback
        and not web
    ):
        return False

    else:
        # django url validator
        url_regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        # if there is one wrong url
        urls = [ios_primary, ios_fallback, android_primary, android_fallback, web]
        for url in urls:
            if not re.match(url_regex, url):
                return False

    return True


def save_url(
    slug, ios_primary, ios_fallback, android_primary, android_fallback, web, db
):
    "Saves the url in db"

    db.execute(
        "INSERT INTO urls( \
                slug, \
                ios_primary_url, \
                ios_fallback_url, \
                android_primary_url, \
                android_fallback_url, \
                web_url \
            ) \
            VALUES(:slug, \
                    :ios_primary_url, \
                    :ios_fallback_url, \
                    :android_primary_url, \
                    :android_fallback_url, \
                    :web_url)",
        {
            "slug": slug,
            "ios_primary_url": ios_primary,
            "ios_fallback_url": ios_fallback,
            "android_primary_url": android_primary,
            "android_fallback_url": android_fallback,
            "web_url": web,
        },
    )

    db.commit()
