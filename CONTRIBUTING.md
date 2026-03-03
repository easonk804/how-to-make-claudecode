# Contributing to How to Make a ClaudeCode

Thank you for your interest in contributing to this AI Agent tutorial project! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/how-to-make-a-claudcode.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run tests: `pytest -q`

## Project Structure

```
how-to-make-a-claudcode/
├── chapters/          # Chapter implementations (01-10)
│   ├── XX_topic/
│   │   ├── README.md
│   │   ├── v1_*.py
│   │   ├── v2_*.py
│   │   ├── v3_*.py
│   │   ├── exercises.md
│   │   └── test_chapterXX.py
├── final/             # End-to-end integration demo
├── tests/             # Cross-chapter tests
├── docs/              # Architecture and roadmap docs
└── knowledge_base/    # RAG demo documents
```

## How to Contribute

### Reporting Issues

When reporting bugs or requesting features, please include:
- A clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Python version and OS
- Relevant code snippets or error messages

### Adding New Chapters

If you want to add a new chapter following our format:

1. Create directory `chapters/XX_topic_name/`
2. Include all required files:
   - `README.md`: Problem intro, evolution, ASCII diagrams, exercises
   - `v1_*.py`: Baseline/minimal implementation
   - `v2_*.py`: First improvement
   - `v3_*.py`: Advanced implementation
   - `exercises.md`: Basic/intermediate/challenge + optional v3 exercises
   - `test_chapterXX.py`: Unit tests using dynamic module loading

3. Follow the teaching principles:
   - One mechanism per chapter (control variables)
   - Minimal runnable code (can be tested without API keys)
   - Progressive improvement (v1 → v2 → v3)
   - ASCII visualizations for concepts
   - Clear, beginner-friendly explanations

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Include docstrings for functions and classes
- Keep functions focused and small
- Use descriptive variable names

### Testing

All contributions must include tests:
- Use `pytest` framework
- Follow existing test patterns (dynamic module loading)
- Ensure tests pass without requiring API keys
- Aim for clear, self-contained test cases

Run tests before submitting:
```bash
pytest -q
```

### Documentation

- Update relevant README files
- Add inline comments for complex logic
- Keep Chinese/English consistent within files
- Include runnable examples

### Commit Messages

Use clear, descriptive commit messages:
```
Add chapter 11: error recovery patterns

- Implement v1: basic error handling
- Add v2: retry with exponential backoff
- Create v3: circuit breaker pattern
- Include tests and exercises
```

## Pull Request Process

1. Ensure tests pass locally: `pytest -q`
2. Update documentation as needed
3. Add a clear PR description explaining changes
4. Link related issues
5. Wait for review and address feedback

## Questions?

Feel free to open an issue for questions or join discussions.

## Code of Conduct

- Be respectful and constructive
- Help others learn
- Focus on educational value
- Keep discussions on-topic

Thank you for helping make AI Agent education better!
