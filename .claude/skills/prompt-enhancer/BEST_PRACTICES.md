# Prompt Enhancement Best Practices

This document outlines proven strategies for transforming beginner-level prompts into senior developer-quality specifications.

## Core Principles

### 1. Clarity Over Brevity
**Bad:** "Fix auth"
**Good:** "Debug and fix JWT token expiration issue in authentication middleware (src/middleware/auth.ts) where tokens are not being refreshed properly after 15 minutes"

Always prefer explicit, detailed descriptions over terse statements.

### 2. Context Before Action
Always establish context before suggesting implementation:
- What exists now?
- What needs to change?
- Why is the change needed?
- What constraints apply?

### 3. Specificity in Requirements
**Vague:** "Make it secure"
**Specific:** 
- Hash passwords with bcrypt (12 salt rounds)
- Implement rate limiting (5 requests per 15 minutes)
- Validate input with Joi schema
- Add CSRF tokens for state-changing operations
- Use parameterized queries to prevent SQL injection

### 4. Measurable Success Criteria
**Weak:** "Should work better"
**Strong:** 
- Response time < 200ms for 95th percentile
- Test coverage > 80%
- Lighthouse performance score > 90
- Zero ESLint errors
- All edge cases handled with proper error messages

## Enhancement Methodology

### Step 1: Decompose the Request

Break down compound requests:

**Input:** "Add user authentication and admin dashboard"

**Decomposed:**
```
Task 1: Implement User Authentication
- Registration endpoint
- Login endpoint
- JWT token generation
- Password hashing
- Session management

Task 2: Create Admin Dashboard
- Admin-only routes
- User management interface
- Activity monitoring
- Analytics visualization

Dependencies:
- Task 2 requires Task 1 completion
- Authentication must include role-based access control
```

### Step 2: Fill Information Gaps

Identify and address missing details:

| Missing Info | Default Assumption | Better Approach |
|--------------|-------------------|-----------------|
| Which files? | Suggest logical location | Check existing structure |
| What dependencies? | Common libraries | Check package.json |
| What style? | Generic code | Match existing patterns |
| What tests? | None specified | Suggest relevant test cases |
| Error handling? | Basic try-catch | Comprehensive error strategy |

### Step 3: Add Technical Depth

Transform surface-level requests into technical specifications:

**Surface Level:** "Add a database"

**Technical Depth:**
```
Database Implementation Plan:

1. Technology Selection:
   - Database: PostgreSQL 15
   - ORM: Prisma 5.x
   - Migration tool: Prisma Migrate

2. Schema Design:
   ```prisma
   model User {
     id        String   @id @default(uuid())
     email     String   @unique
     createdAt DateTime @default(now())
     
     @@index([email])
     @@map("users")
   }
   ```

3. Connection Setup:
   - Connection string in .env
   - Connection pooling (max: 20 connections)
   - Retry logic for transient failures
   - Query timeout: 30 seconds

4. Migration Strategy:
   - Development: prisma migrate dev
   - Production: prisma migrate deploy
   - Rollback plan for failed migrations

5. Seed Data:
   - Script: prisma/seed.ts
   - Test users for development
   - Run: prisma db seed
```

### Step 4: Include Implementation Guidance

Provide clear next steps:

```
Implementation Order:

1. Set up database connection (15 min)
   - Install dependencies: npm install prisma @prisma/client
   - Initialize: npx prisma init
   - Configure DATABASE_URL in .env

2. Define schema (30 min)
   - Create models in schema.prisma
   - Add indexes for performance
   - Document relationships

3. Generate and run migrations (10 min)
   - Generate: npx prisma migrate dev --name init
   - Review generated SQL
   - Apply to database

4. Set up Prisma client (10 min)
   - Create src/lib/db.ts
   - Export singleton instance
   - Add to dependency injection

5. Create repository layer (45 min)
   - Abstract database operations
   - Add error handling
   - Implement CRUD methods

6. Write tests (60 min)
   - Unit tests for repositories
   - Integration tests with test database
   - Mock external dependencies

Total estimated time: ~3 hours
```

## Common Prompt Patterns and Solutions

### Pattern 1: "Make it look like..."

**Input:** "Make it look like Airbnb"

**Enhanced:**
```
Implement visual design inspired by Airbnb's design system:

Layout:
- Max content width: 1280px
- Grid system: 12 columns with 24px gutters
- Spacing scale: 8px base unit (8, 16, 24, 32, 48, 64)

Typography:
- Font family: 'Inter' for body, 'Circular' for headings
- Heading sizes: 32px (h1), 24px (h2), 20px (h3)
- Body: 16px with 1.5 line height
- Font weights: 400 (regular), 600 (semibold), 700 (bold)

Colors:
- Primary: #FF385C (Airbnb red)
- Background: #FFFFFF
- Text: #222222
- Muted text: #717171
- Border: #DDDDDD
- Hover: #E31C5F

Components to implement:
1. Navigation header with search bar
2. Card layout for listings (4 columns on desktop)
3. Image carousel with rounded corners (12px radius)
4. Hover effects (scale 1.02, shadow increase)
5. Button styles (primary, secondary, text)

Responsive breakpoints:
- Mobile: < 768px (1 column)
- Tablet: 768px - 1024px (2 columns)
- Desktop: > 1024px (4 columns)

Accessibility:
- WCAG AA contrast ratios
- Focus indicators on all interactive elements
- Alt text for all images
- Keyboard navigation support
```

### Pattern 2: "Optimize..."

**Input:** "Optimize the code"

**Enhanced:**
```
Code Optimization Plan with Benchmarks:

Current Performance Issues:
- Function `calculateTotal` runs in O(n²) time
- Unnecessary re-renders in React component
- Large bundle size (2.3 MB uncompressed)
- Blocking synchronous operations

Optimization Strategies:

1. Algorithm Optimization:
   ```typescript
   // Before: O(n²)
   const calculateTotal = (items) => {
     return items.map(item => 
       items.filter(i => i.category === item.category)
            .reduce((sum, i) => sum + i.price, 0)
     );
   };
   
   // After: O(n)
   const calculateTotal = (items) => {
     const categoryTotals = items.reduce((acc, item) => {
       acc[item.category] = (acc[item.category] || 0) + item.price;
       return acc;
     }, {});
     return items.map(item => categoryTotals[item.category]);
   };
   ```

2. React Optimization:
   - Add React.memo for pure components
   - Use useCallback for event handlers
   - Implement useMemo for expensive calculations
   - Split large components
   - Use lazy loading for routes

3. Bundle Optimization:
   - Code splitting with dynamic imports
   - Tree shaking unused exports
   - Replace moment.js with date-fns (saves 200kb)
   - Use production builds
   - Enable Gzip compression

4. Async Operations:
   - Move blocking work to Web Workers
   - Use requestIdleCallback for non-urgent tasks
   - Implement debouncing for user input
   - Add loading states

Performance Targets:
- Reduce bundle size to < 500kb
- First Contentful Paint < 1.5s
- Time to Interactive < 3s
- Function execution time < 10ms

Measurement:
- Before optimization: npm run benchmark
- After each change: compare metrics
- Use Chrome DevTools Performance tab
- Add performance.mark() for critical paths
```

### Pattern 3: "Add error handling"

**Input:** "Add error handling"

**Enhanced:**
```
Comprehensive Error Handling Strategy:

Error Categories:

1. Validation Errors (400):
   ```typescript
   class ValidationError extends Error {
     constructor(public field: string, message: string) {
       super(message);
       this.name = 'ValidationError';
     }
   }
   
   // Usage
   if (!email.includes('@')) {
     throw new ValidationError('email', 'Invalid email format');
   }
   ```

2. Authentication Errors (401):
   ```typescript
   class UnauthorizedError extends Error {
     constructor(message = 'Authentication required') {
       super(message);
       this.name = 'UnauthorizedError';
     }
   }
   ```

3. Authorization Errors (403):
   ```typescript
   class ForbiddenError extends Error {
     constructor(resource: string) {
       super(`Access denied to ${resource}`);
       this.name = 'ForbiddenError';
     }
   }
   ```

4. Not Found Errors (404):
   ```typescript
   class NotFoundError extends Error {
     constructor(resource: string, id: string) {
       super(`${resource} with id ${id} not found`);
       this.name = 'NotFoundError';
     }
   }
   ```

5. Server Errors (500):
   ```typescript
   class InternalServerError extends Error {
     constructor(message: string, public originalError?: Error) {
       super(message);
       this.name = 'InternalServerError';
     }
   }
   ```

Global Error Handler:
```typescript
// src/middleware/errorHandler.ts
export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // Log error
  logger.error({
    name: err.name,
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
  });

  // Don't leak error details in production
  const isDevelopment = process.env.NODE_ENV === 'development';

  if (err instanceof ValidationError) {
    return res.status(400).json({
      error: 'Validation failed',
      field: err.field,
      message: err.message,
    });
  }

  if (err instanceof UnauthorizedError) {
    return res.status(401).json({
      error: 'Unauthorized',
      message: err.message,
    });
  }

  if (err instanceof ForbiddenError) {
    return res.status(403).json({
      error: 'Forbidden',
      message: err.message,
    });
  }

  if (err instanceof NotFoundError) {
    return res.status(404).json({
      error: 'Not found',
      message: err.message,
    });
  }

  // Default to 500
  res.status(500).json({
    error: 'Internal server error',
    message: isDevelopment ? err.message : 'An error occurred',
    ...(isDevelopment && { stack: err.stack }),
  });
};
```

Frontend Error Boundary (React):
```tsx
class ErrorBoundary extends React.Component<Props, State> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error reporting service
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorFallback 
          error={this.state.error}
          resetError={() => this.setState({ hasError: false })}
        />
      );
    }

    return this.props.children;
  }
}
```

Async Error Handling:
```typescript
// Wrapper for async route handlers
const asyncHandler = (fn: RequestHandler): RequestHandler => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// Usage
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  if (!user) {
    throw new NotFoundError('User', req.params.id);
  }
  res.json(user);
}));
```

Retry Logic for Network Requests:
```typescript
async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries = 3,
  delay = 1000
): Promise<Response> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
      
      // Don't retry client errors (4xx)
      if (response.status >= 400 && response.status < 500) {
        throw new Error(`Client error: ${response.status}`);
      }
      
      // Retry server errors (5xx)
      if (i === maxRetries - 1) {
        throw new Error(`Server error after ${maxRetries} retries`);
      }
      
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
    }
  }
  throw new Error('Max retries exceeded');
}
```
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Over-Engineering

**Bad:**
```
"Implement a microservices architecture with:
- Event sourcing
- CQRS pattern
- Kubernetes orchestration
- Service mesh
- Distributed tracing
- Circuit breakers
...for a simple CRUD app with 10 users"
```

**Good:**
```
"Implement a REST API with Express.js:
- CRUD endpoints for users
- SQLite database (easy local dev)
- Basic authentication
- Simple validation
Can scale later if needed."
```

### ❌ Anti-Pattern 2: Assumed Knowledge

**Bad:**
```
"Implement the observer pattern with reactive streams"
```

**Good:**
```
"Implement an event system where:
- Components can subscribe to events (like 'userLoggedIn')
- When an event fires, all subscribers get notified
- Subscribers can unsubscribe

Example implementation:
```typescript
class EventEmitter {
  private events: Record<string, Function[]> = {};
  
  on(event: string, callback: Function) {
    if (!this.events[event]) this.events[event] = [];
    this.events[event].push(callback);
  }
  
  emit(event: string, data?: any) {
    this.events[event]?.forEach(cb => cb(data));
  }
}
```
```

### ❌ Anti-Pattern 3: Missing Context

**Bad:**
```
"Use the same pattern as before"
```

**Good:**
```
"Use the repository pattern we implemented in src/repositories/UserRepository.ts:
- Create src/repositories/ProductRepository.ts
- Implement the same methods: findAll(), findById(), create(), update(), delete()
- Use the same error handling approach
- Follow the same TypeScript interface structure"
```

## Prompt Quality Checklist

Before presenting an enhanced prompt, verify:

- [ ] **Specificity**: No ambiguous terms or vague requirements
- [ ] **Context**: Project structure and existing code referenced
- [ ] **Completeness**: All necessary details included
- [ ] **Actionability**: Clear implementation steps provided
- [ ] **Constraints**: Technical limitations and requirements specified
- [ ] **Success criteria**: Measurable outcomes defined
- [ ] **Error handling**: Edge cases and errors addressed
- [ ] **Testing**: Test cases or testing strategy mentioned
- [ ] **Documentation**: Need for comments or docs stated
- [ ] **Maintainability**: Code quality and future changes considered

## Example Quality Comparison

### Low Quality Enhancement
```
User: "add login"

Enhanced: "Add a login page with email and password fields. 
When submitted, check credentials and redirect to dashboard."
```

**Issues:**
- Missing technical details (framework, auth method)
- No error handling specified
- No validation mentioned
- No security considerations
- No file locations
- No success criteria

### High Quality Enhancement
```
User: "add login"

Enhanced: "Implement JWT-based authentication for the Next.js app:

Files to create/modify:
- src/app/login/page.tsx (login UI)
- src/app/api/auth/login/route.ts (login endpoint)
- src/middleware.ts (auth middleware)
- src/lib/auth.ts (JWT utilities)

Login Page (src/app/login/page.tsx):
```tsx
'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || 'Login failed');
      }

      router.push('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div role="alert">{error}</div>}
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        aria-label="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        aria-label="Password"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

API Endpoint (src/app/api/auth/login/route.ts):
- Validate email and password format
- Query database for user
- Compare password with bcrypt
- Generate JWT with 15-minute expiry
- Return JWT in httpOnly cookie
- Return 401 for invalid credentials
- Rate limit: 5 attempts per 15 minutes per IP

Security:
- Use bcrypt.compare() for password verification
- JWT stored in httpOnly, secure, sameSite cookie
- Include CSRF token
- Log failed login attempts
- Lock account after 5 failed attempts

Success Criteria:
- User can log in with valid credentials
- Invalid credentials show error message
- JWT persists across page reloads
- Session expires after 15 minutes
- Works on mobile and desktop
- Passes accessibility audit (WCAG AA)
```

**Strengths:**
- Complete file structure
- Actual code examples
- Security considerations
- Error handling
- Accessibility
- Success criteria
- Rate limiting
- Testing suggestions

## Final Recommendations

1. **Always start with context analysis** - Use CONTEXT_ANALYSIS.md workflow
2. **Reference real examples** - Show similar code from project
3. **Provide escape hatches** - Offer alternatives for complex requirements
4. **Stay humble** - Ask for confirmation before proceeding
5. **Iterate based on feedback** - Adjust enhancement based on user response
6. **Keep user intent sacred** - Never change core requirements
7. **Balance detail with clarity** - Be thorough but not overwhelming
8. **Think production-ready** - Include error handling, testing, security by default
