# CLAUDE.md

This file provides guidance for AI assistants (e.g., Claude Code) working in this repository.

## Repository Overview

**newrepo** is a new, minimal repository currently in its initial state. It contains only a README at this time.

- **Language/Stack:** Not yet determined
- **Purpose:** novo repositorio (new repository — purpose to be defined)

## Repository Structure

```
newrepo/
├── README.md       # Project description
└── CLAUDE.md       # This file — AI assistant guidance
```

As the project grows, update this section to reflect the actual structure.

## Development Workflow

### Branching

- Work on feature branches, never directly on `main` or `master`.
- Branch naming convention: `<type>/<short-description>` (e.g., `feat/add-auth`, `fix/login-bug`).

### Commits

- Write clear, descriptive commit messages in the imperative mood (e.g., "Add login endpoint").
- Keep commits focused — one logical change per commit.

### Pull Requests

- Open a PR against `main` for all changes.
- Include a summary of what changed and why.

## Key Conventions

- Keep the README.md up to date with the project purpose and setup instructions.
- Update this CLAUDE.md file whenever the project structure, stack, or workflows change significantly.

## Getting Started

As of the initial commit, no build or install steps are required. Once dependencies or a build system are added, document the setup steps here, for example:

```bash
# Install dependencies
npm install   # or pip install -r requirements.txt, etc.

# Run tests
npm test

# Start development server
npm run dev
```
