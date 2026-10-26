<!--
SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>

SPDX-License-Identifier: GPL-3.0-only
-->

{% if slide %}
### Importing a page


 ```{admonition} Folder structure
 :class: tip, margin

 ```markdown
 📂content
 ┣ 📄index.md
 ┗ 📂 mypage
    ┣ 📄index.md
    ┣ 📄slide1.md
    ┣ 📄slide2.md
    ┣ 📄slide3.md
    ┗ 📂figures
      ┗ 📊figure1.png
```
{% endif %}

Add the pages `📂mypage/📄index.md` in 
`📂content/📄index.md`:

:::{card} `📂content/📄index.md`
    ```{toctree}
    :maxdepth: {% if slide %}1{% else %}2{% endif %}
    :caption: MyCourse
    
    mypage/index
    ```
:::


