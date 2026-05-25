# Contributing to LazyOwn

Thank you for your interest in contributing to LazyOwn. To ensure the contribution process is as smooth and effective as possible, please follow these guidelines.

## How to Contribute

### Reporting Issues

1. **Check existing issues**: Before opening a new issue, review existing issues to avoid duplicates.
2. **Create a new issue**: If you do not find a similar issue, open a new one. Provide as much detailed information as possible, including steps to reproduce the problem, the environment in which it occurs, and any other relevant information.

### Proposing New Features

1. **Prior discussion**: Before implementing a new feature, open an issue to discuss your idea with maintainers and other contributors.
2. **Specification**: Clearly describe the proposed feature, how it fits into the project, and any additional benefits it might provide.

### Making Changes

1. **Fork the repository**: Fork the repository to your own GitHub account.
2. **Create a branch**: Create a new branch from `dev` for your change (`git checkout dev && git checkout -b feature/new-feature`).
3. **Make changes**: Make your changes in your branch. Ensure you follow the project's coding conventions.
4. **Test**: Ensure your changes do not break anything and that everything works as expected. Add tests if necessary.
5. **Commit**: Commit your changes with descriptive messages (`git commit -m "Description of change"`).
6. **Pull Request**: Open a pull request to the `dev` branch of the original repository. Describe in detail the changes you made and why. Promotions from `dev` to `pp` and `main` are handled by maintainers.

## Branching Model

LazyOwn uses three branches:

- `dev` — active development. All feature branches target this branch.
- `pp` — pre-production / staging. Merged from `dev` after QA.
- `main` — production releases. Merged from `pp` only for tagged releases.

Never commit directly to `main` or `pp`. If you need to hotfix production, branch from `main`, fix, PR to `main`, then back-merge to `pp` and `dev`.

## Coding Standards

- Follow the project's coding conventions.
- Keep your code clean and well documented.
- Ensure your code passes all existing tests and add new tests if necessary.

## Code Reviews

All pull requests will be reviewed by project maintainers. Here are some things we look for in a code review:

- **Code Quality**: Code must be clean, readable, and follow project conventions.
- **Tests**: Ensure all tests pass and new tests have been added for introduced changes.
- **Documentation**: Significant changes must be well documented.

## Communication

Maintain open and respectful communication with other contributors and maintainers. If you have questions, do not hesitate to ask in the project's discussions.

Thank you for contributing to LazyOwn. Together, we can make this project even better.
