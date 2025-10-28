# Context Analysis Guide

This guide provides systematic approaches for analyzing project context before enhancing user prompts.

## Context Discovery Framework

### Level 1: Project Type Identification

Run these commands to identify the project ecosystem:

```bash
# Check for Node.js/JavaScript projects
test -f package.json && echo "Node.js detected" && cat package.json | jq '.dependencies, .devDependencies'

# Check for Python projects
test -f requirements.txt && echo "Python (pip) detected" && head -20 requirements.txt
test -f pyproject.toml && echo "Python (poetry) detected" && cat pyproject.toml
test -f setup.py && echo "Python (setuptools) detected"
test -f Pipfile && echo "Python (pipenv) detected"

# Check for other languages
test -f Cargo.toml && echo "Rust detected"
test -f go.mod && echo "Go detected"
test -f pom.xml && echo "Java (Maven) detected"
test -f build.gradle && echo "Java (Gradle) detected"
test -f Gemfile && echo "Ruby detected"
test -f composer.json && echo "PHP detected"
```

### Level 2: Framework Detection

```bash
# Frontend frameworks
if grep -q "\"react\"" package.json 2>/dev/null; then
  echo "React detected"
  grep -q "\"next\"" package.json && echo "Next.js detected"
fi

if grep -q "\"vue\"" package.json 2>/dev/null; then
  echo "Vue detected"
  grep -q "\"nuxt\"" package.json && echo "Nuxt detected"
fi

grep -q "\"@angular/core\"" package.json 2>/dev/null && echo "Angular detected"
grep -q "\"svelte\"" package.json 2>/dev/null && echo "Svelte detected"

# Backend frameworks
grep -q "\"express\"" package.json 2>/dev/null && echo "Express detected"
grep -q "\"fastify\"" package.json 2>/dev/null && echo "Fastify detected"
grep -q "\"nestjs\"" package.json 2>/dev/null && echo "NestJS detected"

# Python frameworks
grep -q "django" requirements.txt 2>/dev/null && echo "Django detected"
grep -q "flask" requirements.txt 2>/dev/null && echo "Flask detected"
grep -q "fastapi" requirements.txt 2>/dev/null && echo "FastAPI detected"
```

### Level 3: Project Structure Analysis

```bash
# Analyze directory structure
echo "=== Directory Structure ==="
tree -L 2 -d 2>/dev/null || find . -maxdepth 2 -type d

# Find entry points
echo "=== Entry Points ==="
find . -name "index.*" -o -name "main.*" -o -name "app.*" | head -10

# Check for configuration files
echo "=== Configuration Files ==="
ls -la | grep -E "\.config\.|\.rc|\.json$|\.ya?ml$"

# Identify source directories
echo "=== Source Directories ==="
ls -d src/ app/ lib/ components/ pages/ api/ 2>/dev/null
```

### Level 4: Dependency and Tooling

```bash
# TypeScript or JavaScript?
test -f tsconfig.json && echo "TypeScript project"

# Build tools
test -f vite.config.* && echo "Using Vite"
test -f webpack.config.* && echo "Using Webpack"
test -f rollup.config.* && echo "Using Rollup"

# Testing frameworks
grep -q "jest" package.json 2>/dev/null && echo "Jest detected"
grep -q "vitest" package.json 2>/dev/null && echo "Vitest detected"
grep -q "pytest" requirements.txt 2>/dev/null && echo "Pytest detected"

# Linting/Formatting
test -f .eslintrc.* && echo "ESLint configured"
test -f .prettierrc.* && echo "Prettier configured"
test -f .ruff.toml && echo "Ruff (Python linter) configured"
```

## Context Extraction Templates

### For React/Next.js Projects

```bash
# Get project structure
cat package.json | jq '{
  name, version, 
  dependencies: .dependencies | keys,
  devDependencies: .devDependencies | keys,
  scripts
}'

# Check routing setup
if [ -d "app" ]; then
  echo "App Router (Next.js 13+)"
  find app -name "page.*" -o -name "layout.*" | head -10
elif [ -d "pages" ]; then
  echo "Pages Router"
  find pages -name "*.tsx" -o -name "*.jsx" | head -10
fi

# Check for state management
grep -q "redux" package.json && echo "Redux detected"
grep -q "zustand" package.json && echo "Zustand detected"
grep -q "jotai" package.json && echo "Jotai detected"
grep -q "recoil" package.json && echo "Recoil detected"

# Check for styling approach
grep -q "tailwindcss" package.json && echo "Tailwind CSS"
grep -q "styled-components" package.json && echo "Styled Components"
grep -q "@mui/material" package.json && echo "Material-UI"
grep -q "@chakra-ui" package.json && echo "Chakra UI"
```

### For Backend Projects

```bash
# API framework identification
if [ -f "src/main.ts" ] || [ -f "src/app.ts" ]; then
  echo "TypeScript backend detected"
  head -20 src/main.ts 2>/dev/null || head -20 src/app.ts
fi

# Database detection
grep -q "prisma" package.json 2>/dev/null && echo "Prisma ORM" && cat prisma/schema.prisma 2>/dev/null | head -30
grep -q "typeorm" package.json 2>/dev/null && echo "TypeORM"
grep -q "mongoose" package.json 2>/dev/null && echo "Mongoose (MongoDB)"
grep -q "pg" package.json 2>/dev/null && echo "PostgreSQL (pg driver)"
grep -q "mysql2" package.json 2>/dev/null && echo "MySQL"

# Check environment setup
if [ -f ".env.example" ]; then
  echo "=== Environment Variables Template ==="
  cat .env.example
fi
```

### For Python Projects

```bash
# Virtual environment check
test -d "venv" && echo "venv detected" || echo "No venv found"
test -d ".venv" && echo ".venv detected"

# Framework detection
if grep -q "django" requirements.txt 2>/dev/null; then
  echo "Django project"
  find . -name "settings.py" | head -3
  find . -name "urls.py" | head -5
fi

if grep -q "fastapi" requirements.txt 2>/dev/null; then
  echo "FastAPI project"
  find . -name "main.py" | head -3
fi

# Check for async code
grep -rn "async def" --include="*.py" | head -5 && echo "Async code detected"
```

## Coding Style Detection

### Extract Style Rules

```bash
# TypeScript/JavaScript style
if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ]; then
  echo "=== ESLint Rules ==="
  cat .eslintrc.* | head -50
fi

if [ -f ".prettierrc" ]; then
  echo "=== Prettier Config ==="
  cat .prettierrc
fi

# Python style
if [ -f "pyproject.toml" ]; then
  echo "=== Python Style Config ==="
  grep -A 10 "\[tool\." pyproject.toml
fi

# Check for EditorConfig
if [ -f ".editorconfig" ]; then
  echo "=== EditorConfig ==="
  cat .editorconfig
fi
```

### Infer from Existing Code

```bash
# Indentation style
echo "=== Indentation Analysis ==="
head -100 src/**/*.ts 2>/dev/null | grep -o "^[[:space:]]*" | sort | uniq -c

# Quote style
echo "=== Quote Style ==="
grep -rh "import.*from" src/ 2>/dev/null | head -20 | grep -o "['\"]" | sort | uniq -c

# Naming conventions
echo "=== Common Patterns ==="
grep -rh "^(export )?const " src/ 2>/dev/null | head -20
grep -rh "^(export )?function " src/ 2>/dev/null | head -20
```

## Git Context

```bash
# Recent changes
echo "=== Recent Commits ==="
git log --oneline -10 2>/dev/null

# Current branch
echo "=== Current Branch ==="
git branch --show-current 2>/dev/null

# Uncommitted changes
echo "=== Uncommitted Changes ==="
git status -s 2>/dev/null

# Find recently modified files
echo "=== Recently Modified Files ==="
git ls-files -m 2>/dev/null || find . -type f -mtime -1 | grep -v node_modules | head -20
```

## Documentation Discovery

```bash
# README analysis
if [ -f "README.md" ]; then
  echo "=== README Overview ==="
  head -50 README.md
fi

# Check for other documentation
echo "=== Documentation Files ==="
find . -name "*.md" | grep -v node_modules | head -10

# API documentation
find . -name "swagger.*" -o -name "openapi.*" | head -5
```

## Common Project Patterns

### Monorepo Detection

```bash
# Check for monorepo tools
test -f "pnpm-workspace.yaml" && echo "pnpm workspace detected"
test -f "lerna.json" && echo "Lerna monorepo detected"
test -f "turbo.json" && echo "Turborepo detected"
test -f "nx.json" && echo "Nx monorepo detected"

# List packages
if [ -d "packages" ]; then
  echo "=== Packages ==="
  ls -d packages/*/
fi
```

### Microservices Architecture

```bash
# Check for service directories
if [ -d "services" ] || [ -d "apps" ]; then
  echo "=== Services/Apps ==="
  ls -d services/*/ apps/*/ 2>/dev/null
  
  # Check for Docker
  find . -name "Dockerfile" | head -10
  find . -name "docker-compose.yml"
fi
```

## Context Summary Template

After gathering context, structure it as:

```markdown
## Project Context Summary

### Technology Stack
- Language: [TypeScript/JavaScript/Python/etc]
- Runtime: [Node.js 18/Python 3.11/etc]
- Framework: [Next.js 14/FastAPI/Django/etc]
- Database: [PostgreSQL/MongoDB/etc]

### Project Structure
- Entry point: [src/main.ts]
- Source directory: [src/]
- Routing: [App Router/Pages Router/etc]
- Key directories: [components/, api/, lib/]

### Development Setup
- Package manager: [npm/pnpm/yarn]
- Build tool: [Vite/Webpack/etc]
- Testing: [Jest/Vitest/Pytest]
- Linting: [ESLint/Ruff]
- Formatting: [Prettier/Black]

### Code Style Conventions
- Indentation: [2 spaces/4 spaces/tabs]
- Quotes: [single/double]
- Semicolons: [yes/no]
- Naming: [camelCase/PascalCase/snake_case]

### Current State
- Branch: [main/feature-x]
- Recent changes: [what was recently modified]
- Uncommitted work: [any local changes]

### Dependencies Relevant to Request
- [List specific libraries that relate to user's request]
```

## Context-Based Enhancement Strategies

### Strategy 1: Match Existing Patterns

```bash
# Find similar implementations
grep -rn "similar_pattern" src/ | head -10

# Example: Find existing API routes
find . -name "*.route.ts" -o -name "*.routes.ts" | head -10

# Example: Find existing components
find . -path "*/components/*.tsx" | head -20
```

### Strategy 2: Respect Project Conventions

```bash
# File naming
ls src/**/*.ts | sed 's/.*\///' | grep -o "[a-z-]*\..*" | head -20

# Export style
grep -rh "^export " src/ | head -20 | sort | uniq -c
```

### Strategy 3: Leverage Existing Infrastructure

```bash
# Check for shared utilities
ls -la src/utils/ src/lib/ src/helpers/ 2>/dev/null

# Check for shared types
find . -name "types.ts" -o -name "*.types.ts" | head -10

# Check for existing hooks (React)
find . -path "*/hooks/*.ts" -o -path "*/hooks/*.tsx" | head -10
```

## Red Flags to Check

```bash
# Security concerns
echo "=== Security Check ==="
grep -rn "process.env" src/ | grep -v "NODE_ENV" | head -5
grep -rn "eval(" src/ | head -5
grep -rn "dangerouslySetInnerHTML" src/ | head -5

# Performance concerns
echo "=== Performance Check ==="
grep -rn "console.log" src/ | wc -l
find . -name "*.jpg" -o -name "*.png" | head -10 | xargs ls -lh

# Code quality concerns
echo "=== Code Quality Check ==="
find src/ -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -rn | head -10
```

## Using Context in Enhancement

When enhancing a prompt, reference discovered context:

```
"Based on your Next.js 14 App Router setup and existing Prisma schema..."
"Following the camelCase convention I see in your codebase..."
"Using the error handling pattern from your existing API routes..."
"Matching the component structure in your components/ui directory..."
```

This shows the user you've analyzed their project and are providing contextually appropriate guidance.
