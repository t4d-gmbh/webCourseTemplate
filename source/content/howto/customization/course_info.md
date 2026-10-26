<!--
SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>

SPDX-License-Identifier: GPL-3.0-only
-->

### Course Information

{% if page %}
Finally, you need to set some project specific information, that is the name of
your project, as well as, authorship and copyright informaiton.

The **project name** must be set with the setting `project` and will only set the
`title` tag in the HTML header.
In case this does not speak to you at all, simply set the `project` setting to
the actual name of your web-course, e.g.:
{% else %}
Set the `project` name (e.g.):
{% endif %}

```python
project = 'My Intro To 🌐 Dominance'
```

{% if page %}
**Authorship** information needs to be provided as an unstructured string with the
`author` setting. We recommend to provide a comma separated list of full names
along with a link to further information about the person (e.g. email or link
to GitHub profile),
e.g.:
{% else %}
Set the `author`-ship information (e.g.):
{% endif %}

```python
author = 'Jon Doe - jon@doe.com, Marvin a depressed Android - github.com/marvin-android'
```

{% if page %}
The **copyright** notice can be adapted if needed, it should contain at least
the name of a natural or legal person.
If you leave the `copyright` setting unchanged, it will show the current year
and the repository owner.
To write a custom copyright message use:
{% else %}
Optionally adapt the `copyright` information (e.g.):
{% endif %}

:::{note}
:class: margin

We recommend to leave the `copyright` setting unchanged.
:::
```python
copyright = '1979, Jon Doe'
```

