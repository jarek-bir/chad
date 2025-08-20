# Contributing to Chad

We love your input! We want to make contributing to Chad as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issues](https://github.com/ivan-sincek/chad/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/ivan-sincek/chad/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Code Style Guidelines

- Use consistent indentation (tabs or spaces, pick one)
- Follow PEP 8 for Python code
- Add docstrings to functions and classes
- Use meaningful variable and function names
- Comment complex logic

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Install in development mode: `pip install -e .`

## Testing

Before submitting a pull request:

1. Test your changes with various Google Dorks
2. Ensure rate limiting works properly
3. Test with and without proxies
4. Verify Chad Extractor functionality if applicable

## Adding New Features

When adding new features:

1. Update the help text in `validate.py`
2. Update the README.md
3. Add appropriate error handling
4. Consider rate limiting implications
5. Test thoroughly

## Code of Conduct

Be respectful and constructive in all interactions.
