# Contributing to Omni-Sentinel

Thank you for your interest in contributing to Omni-Sentinel! We welcome contributions from the community to help make this project more robust and secure.

## Security-Sensitive Contributions

This project handles high-assurance governance and cryptographic modules (PQC/ML-DSA). Any changes to the following modules require mandatory review by at least two maintainers and must include formal verification or exhaustive testing:
- `src/infrastructure/pqc_worm_logger.py`
- `src/governance_engine/zkml_pipeline_verifier.py`

## How to Contribute

1.  **Report Bugs**: If you find a bug, please open an issue. Include a detailed description and steps to reproduce.
2.  **Suggest Features**: Open an issue to discuss new feature ideas.
3.  **Submit Pull Requests**:
    - Fork the repository.
    - Create a new branch using the convention: `feature/<description>`, `bugfix/<description>`, or `security/<description>`.
    - Sign off your commits using `git commit -s` to indicate DCO compliance.
    - Write tests for your changes.
    - Ensure all tests pass.
    - Submit a PR with a clear description.

## Coding Standards

- Follow PEP 8 for Python code.
- Use type hints for all public APIs.
- Ensure all functions and classes have descriptive docstrings.

## Testing

Always run the full test suite before submitting a pull request:

```bash
python3 -m pytest tests/
```

## Community

Join our community discussions and help us build a safer environment for cognitive agents!

## Security Disclosure

If you discover a security vulnerability, please refer to our [SECURITY.md](SECURITY.md) for reporting instructions. Do not open public issues for security vulnerabilities.
