# Web Course Template

This is <img src="./source/_static/T4D_logo.svg" alt="T4D" width="25" height="25">'s template for a web-based
course/workshop content.

Feel free to reuse the template under its licence, but please replace or remove
our logos (the T4D's) before publishing your own course.

---

_If you find this template useful, please share it with others! Show your support by giving it a 🌟 using the ⭐-button at the top right of the page._

---

## Usage 🛠️

You can simply [use this repository as a template](https://github.com/new?template_name=web-course-template&template_owner=t4d-gmbh) for your own project.

The **actual content** of the web-based course resides under `./source/content` folder.
There you find the content for the documentation of this template which should serve you both as 🧭 guideline and 💡 inspiration.
The **design** of the web course is defined in `./source/conf.py` file.
<!-- include-upper -->

Head over to the [online documentation](https://t4d-gmbh.github.io/webCourseTemplate/) for detailed instructions how to build your own web course.

### Quickstart

1. Clone the repository
2. Create/activate your virtual environment running python3.13 (we recommend using `uv` for this).
3. Install the dependencies from `requirements.txt`
4. Edit the content.
5. Build the pages locally with:  
   ```
   sphinx-build -b html source docs/html -E -A build="pages"
   ```
   And the slides:
   ```
   sphinx-build -b html source docs/html/slides -E -A build="slides"
   ```
6. View your course locally by opening the files: `docs/html/index.hmtl` (pages) and `docs/html/slides/index.html` for the slides.

## License

The template is licensed under [GPL-3.0-only](LICENSE), with these exceptions:

- **T4D logos:** The files `source/_static/T4D_logo.svg`,
  `source/_static/T4D_logo_bw.svg`, and `source/_static/T4D_logo_wb.svg` are
  excluded from the GPL licence. All rights are reserved; use requires prior
  written permission, except where permitted by applicable law. See
  [the logo terms](LICENSES/LicenseRef-T4D-Logo.txt). Replace or remove these
  logos before publishing a course based on this template.
- **Bundled fonts:** The M+ fonts retain their third-party copyright and
  [SIL Open Font License 1.1](source/_static/fonts/OFL.txt).

## Contributing 🤝🎉

We welcome contributions to this template!
Whether you're fixing bugs 🐛 or typos, adding new features ✨, or improving readability 📚, your help is greatly appreciated!

Before you start, please take a moment to read our [CONTRIBUTING.md](CONTRIBUTING.md) file.
It contains some details and guidelines 📋 on how to structure new content and best practices to help you get started and ensure that your contributions aligned with the project's goals. 🚀

Thank you for considering contributing to this course! You're awesome! 🌟
