<!--
SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>

SPDX-License-Identifier: GPL-3.0-only
-->

### Combining Content

We want to display each slide as a separate site but combine several slides into a single static webpage.

To do so we can use the following pattern in each`index.md` file of a sub-folder in `source/content`:


{% raw %}
    {% if build == "slides" %}
    <!-- BUILDING THE SLIDES -->
    ```{toctree}
    :maxdepth: 2
    :caption: MySubSection
    
    ./slide1
    ./slide2
    ```
    {% else %}
    <!-- BUILDING THE PAGES -->
    ```{include} ./slide1.md
    ```
    ```{include} ./slide2.md
    ```
    {% endif %}
{% endraw %}
