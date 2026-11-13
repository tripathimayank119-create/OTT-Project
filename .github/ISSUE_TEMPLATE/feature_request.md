---
name: Feature Request
description: Feature request to help us improve
title: "[Feature] "
labels: ["feature"]
body:
  - type: input
    attributes:
      label: Feature Description
      description: A clear and concise description of the feature you want.
    validations:
      required: true

  - type: input
    attributes:
      label: Use Case
      description: Explain why this feature is needed and how it would be used.
    validations:
      required: true

  - type: input
    attributes:
      label: Proposed Solution
      description: Think about any solutions you've considered. If no good solution exists, say "N/A".
    validations:
      required: false

  - type: input
    attributes:
      label: Priority
      description: [optional] High / Medium / Low
    validations:
      required: false

  - type: input
    attributes:
      label: Additional Context
      description: Add any other context or screenshots about the feature request here.
    validations:
      required: false
---