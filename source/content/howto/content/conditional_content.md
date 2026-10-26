<!--
SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>

SPDX-License-Identifier: GPL-3.0-only
-->

### Conditional Content

Within each included or imported `.md` file you can also specify what content you want
to show in the slides and what should be shown in the page view.
You can use:

- `{% if builds == 'pages' %}...{% endif %}` or `{% if page %}...{% endif %}` to include
  content only in the static page
- `{% if builds == 'slides' %}...{% endif %}` or `{% if slide %}...{% endif %}` to include
  content only in the slide

The above `slide1.md` could look as follows:

{% raw %}
    {% if build == "slides" %}
    # Slide 1 title
    {% else %}
    ## Subtitle for slide 1 content
    {% endif %}

    **This text is both on the slide and in the pages
    {% if slide %}
    🤪 This in only on the slide 🤪
    {% endif %}

    {% if page %}
    This text is only in the pages view and not on the slide
    {% endif %}
{% endraw %}
