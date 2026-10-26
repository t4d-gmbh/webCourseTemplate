<!--
SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>

SPDX-License-Identifier: GPL-3.0-only
-->

### Custom 🦆Logo🦆

{% if page %}
In order to add your own logo (ideally a file in the `SVG` format) you can add
a file with the logo under `source/_static` and specify the path in the
`course_logo` dictionary.
Say you added the files `my_logo_light.svg` and `my_logo_dark.svg` under 
`./source/_static`, then a valid configuration would look like this:
{% else %}
Add your own logo as an *SVG*-file under `source/_static` and adapt the config:
{% endif %}

:::{admonition} `alt-text`
:class: tip, margin

Simply leave the `alt-text` empty (`"alt-text" = ""`) to avoid showing to avoid
showing some text under (or instead of) the logo.

:::
```python
# ./source/config.py
course_logo = {
    "image_light": "_static/my_logo_light.svg",
    "image_dark": "_static/my_logo_dark.svg",
    "alt-text": "MyLogo",
    "favicon": "_static/my_logo_light.svg",
}
```
