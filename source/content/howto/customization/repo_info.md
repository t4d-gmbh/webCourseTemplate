<!--
SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>

SPDX-License-Identifier: GPL-3.0-only
-->

### Repository Information

{% if page %}
First, you need to make sure that the web-content correctly points to your own
repository.
To do so you will need to set:
{% else %}
Make sure the web-content points to your repository:
{% endif %}

- **`repository_owner`**: Your username or name of the organization your repository belongs to.
- **`repository_name`**: The actual name of your repository
- **`repository_branch`**: The branch you are deploying from.
  {% if page %}If unsure simply set this to `main`.{% endif %}
