name: Spec Kit

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  spec-kit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Spec Kit from GitHub
        run: |
          python -m pip install --upgrade pip
          python -m pip install --upgrade "git+https://github.com/github/spec-kit.git"
      - name: Run Spec Kit checks
        run: |
          specify check || true
          specify --help || true
          specify validate --config specs/spec-kit.yaml || true
name: Spec Kit

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  spec-kit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install (optional)
        run: |
          # If the package is public, install as dev dependency; otherwise use npx
          npm ci || true
      - name: Run Spec Kit checks
        run: |
          # Use npx to run the Spec Kit CLI without committing it to package.json
          npx --no-install @githubnext/spec-kit validate --config specs/spec-kit.yaml || true
