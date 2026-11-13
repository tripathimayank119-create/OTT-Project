---
name: Bug Report
description: File a bug report to help us improve
title: "[Bug] "
labels: ["bug"]
body:
  - type: input
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
    validations:
      required: true

  - type: input
    attributes:
      label: To Reproduce
      description: Steps to reproduce the behavior:
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. See error

  - type: input
    attributes:
      label: Expected Behavior
      description: A clear and concise description of what expected to happen.

  - type: input
    attributes:
      label: Environment
      description:
        - OS: [e.g. macOS, Windows, Linux]
        - Python version: [e.g. 3.12]
        - FastAPI version: [e.g. 0.109.0]
    validations:
      required: false

  - type: input
    attributes:
      label: Additional Context
      description: Add any other context about the problem here.
    validations:
      required: false
---