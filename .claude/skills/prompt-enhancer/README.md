# Prompt Enhancer Skill for Claude Code

A specialized skill that transforms beginner-level development requests into senior developer-quality prompts for Claude Code, enhancing clarity, specificity, and technical accuracy.

## Overview

This skill acts as an intelligent intermediary between the user and Claude Code, analyzing project context and refining requests to ensure optimal implementation outcomes. It bridges the gap between what novice developers ask for and what senior developers would specify.

## What This Skill Does

### Core Capabilities

1. **Context Analysis**
   - Automatically detects project type (React, Next.js, Django, FastAPI, etc.)
   - Identifies existing patterns and conventions
   - Discovers project structure and dependencies
   - Analyzes code style and naming conventions

2. **Request Enhancement**
   - Adds missing technical specifications
   - Clarifies ambiguous requirements
   - Specifies file locations and implementations
   - Includes error handling and edge cases
   - Adds testing requirements
   - Defines success criteria

3. **Best Practice Integration**
   - Suggests appropriate design patterns
   - Includes security considerations
   - Recommends performance optimizations
   - Ensures accessibility compliance
   - Maintains code quality standards

## Installation

### For Claude Code

1. Download the `prompt-enhancer.zip` file
2. Extract to your Claude Code skills directory:
   ```bash
   # Default location
   mkdir -p ~/.claude/skills
   unzip prompt-enhancer.zip -d ~/.claude/skills/
   ```

3. Verify installation:
   ```bash
   ls ~/.claude/skills/prompt-enhancer/
   # Should show: SKILL.md, EXAMPLES.md, CONTEXT_ANALYSIS.md, BEST_PRACTICES.md
   ```

### For Claude.ai

1. Go to Settings → Features → Skills
2. Click "Upload Skill"
3. Select the `prompt-enhancer.zip` file
4. Confirm installation

## How to Use

### Automatic Activation

The skill automatically activates when it detects:
- Vague or ambiguous requests
- Missing technical details
- Requests that could benefit from structure
- Questions about implementation approach

### Example Interactions

#### Example 1: Simple Request → Detailed Specification

**Your input:**
```
add a search feature
```

**What the skill does:**
1. Checks your project structure
2. Identifies framework (e.g., React + TypeScript)
3. Discovers existing UI patterns
4. Analyzes similar components

**Enhanced output:**
```
Implement a real-time search feature for the user list page:

Files to create/modify:
- src/components/UserSearch.tsx (new)
- src/pages/Users.tsx (modify)

Requirements:
1. Search input with Material-UI TextField
2. Debounce input (300ms)
3. Filter by: firstName, lastName, email, role
4. Case-insensitive partial matching
5. Display loading indicator
6. Show "No results found" message

Technical details:
- Use react-query for data fetching
- Endpoint: GET /api/users/search?q={query}
- Cache results for 5 minutes
- ARIA labels for accessibility

Would you like me to proceed with this implementation?
```

#### Example 2: Bug Report → Debug Plan

**Your input:**
```
the app crashes sometimes
```

**Enhanced output:**
```
Let me help you debug this crash. First, I'll gather some information:

[Checks error logs, recent changes, console output]

Based on the error "Maximum call stack size exceeded" in useDataFetch.ts,
here's a systematic debug plan:

Investigation Steps:
1. Check useEffect dependencies for circular updates
2. Add debug logging to track re-render count
3. Review state updates inside effect

Common causes:
- Object in dependency array
- State setter triggering effect
- Missing cleanup function

Proposed fix with example code...

Would you like me to implement this debugging approach?
```

#### Example 3: Performance Request → Optimization Plan

**Your input:**
```
make it faster
```

**Enhanced output:**
```
I'll analyze your current performance and create an optimization plan.

[Runs performance checks, analyzes bundle size, checks images]

Current Performance Issues:
- Homepage LCP: 4.2s (target: < 2.5s)
- Bundle size: 2.3MB (large images, no code splitting)
- Lighthouse score: 45/100

Optimization Plan:
1. Image Optimization (Expected: -40% LCP)
   - Convert to WebP
   - Add Next.js Image component
   - Implement lazy loading

2. Code Splitting (Expected: -1.5MB bundle)
   - Dynamic imports for routes
   - Lazy load heavy components

3. Caching Strategy
   - Implement ISR
   - Add SWR for client data

Implementation timeline: ~3 hours

Shall I proceed with these optimizations?
```

## When the Skill Activates

### High Priority Triggers

The skill immediately activates when requests:
- Lack file paths or locations
- Don't specify error handling
- Are missing validation requirements
- Could benefit from security considerations
- Need performance targets
- Should include tests

### Medium Priority Triggers

The skill may activate when requests:
- Use generic terms ("optimize", "improve", "fix")
- Reference unclear components ("the function", "that page")
- Don't specify success criteria
- Could use existing project patterns

### Won't Activate

The skill stays silent for:
- Very specific, well-formed requests
- Simple questions with clear answers
- Requests that explicitly decline enhancement
- Non-development queries

## Skill Architecture

```
prompt-enhancer/
├── SKILL.md                  # Core enhancement logic and workflow
├── EXAMPLES.md               # Real-world transformation examples
├── CONTEXT_ANALYSIS.md       # Project analysis techniques
├── BEST_PRACTICES.md         # Quality standards and patterns
└── README.md                 # This file
```

### File Purposes

**SKILL.md** (Main Instructions)
- Enhancement methodology
- Context gathering procedures
- Template structures
- Integration workflow

**EXAMPLES.md** (Reference Material)
- Before/after comparisons
- Common patterns
- Enhancement strategies
- Domain-specific examples

**CONTEXT_ANALYSIS.md** (Technical Guide)
- Project detection scripts
- Framework identification
- Style convention discovery
- Git context extraction

**BEST_PRACTICES.md** (Quality Standards)
- Enhancement principles
- Anti-patterns to avoid
- Quality checklists
- Optimization strategies

## Customization

### Adjust Enhancement Level

You can control how detailed the enhancements are:

```bash
# More detail (recommended for beginners)
"Use prompt enhancer with maximum detail"

# Balanced (default)
"Enhance this prompt"

# Minimal (for experienced developers)
"Quick enhancement only"
```

### Override Suggestions

You can always override the enhanced prompt:

```
User: "add login"
Skill: [Provides detailed JWT auth implementation]
User: "Actually, just use simple session-based auth instead"
Skill: [Adjusts to simpler approach]
```

## Advanced Features

### Pattern Learning

The skill learns from your project:
- Detects naming conventions (camelCase vs snake_case)
- Identifies preferred libraries (React Query vs SWR)
- Recognizes file organization patterns
- Adapts to your code style (spaces vs tabs, quotes, etc.)

### Multi-File Operations

For complex requests, the skill provides:
- File creation order
- Dependency setup steps
- Migration strategies
- Testing checkpoints

### Security-First Approach

All enhancements include:
- Input validation
- Error sanitization
- Authentication/authorization checks
- OWASP Top 10 considerations

## Configuration

### Project-Specific Preferences

Create `.claude/config.json` in your project:

```json
{
  "promptEnhancer": {
    "detailLevel": "high",
    "includeTests": true,
    "includeTypeScript": true,
    "securityChecks": true,
    "styleGuide": "airbnb"
  }
}
```

### Global Settings

Edit `~/.claude/skills/prompt-enhancer/config.json`:

```json
{
  "defaultDetailLevel": "medium",
  "alwaysAskBeforeEnhancing": false,
  "preferredFrameworks": {
    "frontend": "react",
    "backend": "express",
    "database": "postgresql"
  }
}
```

## Troubleshooting

### Skill Not Activating

1. Check skill is installed:
   ```bash
   ls ~/.claude/skills/prompt-enhancer/SKILL.md
   ```

2. Verify YAML frontmatter is valid:
   ```bash
   head -5 ~/.claude/skills/prompt-enhancer/SKILL.md
   ```

3. Try explicit trigger:
   ```
   "Use prompt enhancer skill to help with..."
   ```

### Too Much Detail

If enhancements are overwhelming:
```
"Give me a simpler version"
"Just the key points"
"Skip the examples"
```

### Not Enough Detail

If you need more:
```
"Add more implementation details"
"Include code examples"
"Explain the security considerations"
```

## Best Practices for Users

### DO:
✓ Provide context about what you're trying to achieve
✓ Mention any constraints (time, complexity, etc.)
✓ Review enhanced prompts before approving
✓ Give feedback on enhancement quality

### DON'T:
✗ Assume the skill knows unpublished information
✗ Skip the review step
✗ Ignore security suggestions
✗ Override best practices without reason

## Examples by Use Case

### Web Development
- "add authentication" → Full JWT implementation
- "create a form" → Form with validation, error handling, accessibility
- "build an API" → RESTful endpoints with docs, tests, rate limiting

### Database
- "add a users table" → Schema with indexes, migrations, seed data
- "optimize queries" → Analysis, indexes, caching strategy

### Testing
- "add tests" → Unit, integration, E2E test suite with examples

### DevOps
- "deploy this" → Docker setup, CI/CD pipeline, env management

### Mobile
- "make it responsive" → Breakpoints, mobile-first CSS, touch targets

## Version History

- **v1.0.0** (2025-01-26)
  - Initial release
  - Support for React, Next.js, Express, Django, FastAPI
  - Context analysis and enhancement
  - Best practices integration

## Contributing

To improve this skill:

1. Document common request types you encounter
2. Add project-specific patterns to CONTEXT_ANALYSIS.md
3. Share enhancement examples in EXAMPLES.md
4. Report issues or suggest improvements

## License

This skill is provided as-is for use with Claude Code and Claude.ai.

## Support

For issues or questions:
- Check EXAMPLES.md for similar cases
- Review BEST_PRACTICES.md for guidance
- Consult Anthropic's documentation: https://docs.claude.com

---

**Note:** This skill enhances prompts but doesn't replace your judgment. Always review suggestions and adjust based on your specific requirements, constraints, and expertise level.
