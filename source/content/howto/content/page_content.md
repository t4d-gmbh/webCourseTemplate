<!--
SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>

SPDX-License-Identifier: GPL-3.0-only
-->

### Create a 📚 page

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

1. Create a new sub-folder (e.g. `📂 mypage`)
1. Create for each slide a separate file (like `📄slide2.md`)
1. Add `📄index.md` that imports and combines all slides
1. Import `📄mypage/index.md` in the `toctree` in `📄index.md`
