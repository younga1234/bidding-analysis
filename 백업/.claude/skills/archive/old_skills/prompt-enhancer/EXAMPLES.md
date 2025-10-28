# Prompt Enhancement Examples

This document contains real-world examples of prompt transformations from beginner to senior developer level.

## Example 1: Vague Feature Request → Detailed Specification

### Original Request:
```
"Add a search feature"
```

### Context Discovered:
- React + TypeScript project
- Existing UI component library (Material-UI)
- REST API backend
- User list page exists at `src/pages/Users.tsx`

### Enhanced Prompt:
```
Implement a real-time search feature for the user list page:

Location: src/pages/Users.tsx
Component: Create src/components/UserSearch.tsx

Requirements:
1. Search Input Component:
   - Use Material-UI TextField with search icon
   - Debounce input (300ms) to prevent excessive API calls
   - Clear button when text present
   - Placeholder: "Search by name, email, or role..."

2. Search Logic:
   - Filter on: firstName, lastName, email, role
   - Case-insensitive matching
   - Partial match support (includes, not exact)
   - Show loading indicator during search
   - Display "No results found" message

3. API Integration:
   - Endpoint: GET /api/users/search?q={query}
   - Use existing useQuery hook from react-query
   - Handle network errors gracefully
   - Cache results for 5 minutes

4. UX Considerations:
   - Preserve scroll position after search
   - Highlight matching text in results
   - Show result count: "Found X users"
   - Allow clearing search to show all users

TypeScript Interface:
```typescript
interface SearchProps {
  onSearchResults: (users: User[]) => void;
  placeholder?: string;
  debounceMs?: number;
}
```

Accessibility:
- ARIA labels for screen readers
- Keyboard navigation (Escape to clear)
- Focus management
```

---

## Example 2: Bug Report → Systematic Debug Plan

### Original Request:
```
"The app crashes sometimes"
```

### Context Discovered:
- Error log shows "Maximum call stack size exceeded"
- Occurs in React useEffect
- File: src/hooks/useDataFetch.ts

### Enhanced Prompt:
```
Debug and fix the infinite loop causing stack overflow in useDataFetch hook:

File: src/hooks/useDataFetch.ts

Symptoms:
- "Maximum call stack size exceeded" error
- Occurs intermittently on data fetch
- Browser tab becomes unresponsive
- Memory usage spikes before crash

Investigation Steps:

1. Analyze useEffect Dependencies:
   ```typescript
   // Check current dependencies array
   useEffect(() => {
     // fetch logic
   }, [dependencies]); // ← Review this
   ```
   - Look for object/array dependencies causing re-renders
   - Check if state setters are in dependency array
   - Verify ref stability

2. Add Debug Logging:
   ```typescript
   useEffect(() => {
     console.count('useDataFetch render');
     console.log('Dependencies changed:', { /* list deps */ });
     // existing code
   }, [dependencies]);
   ```

3. Common Causes to Check:
   - State updates inside useEffect without proper conditions
   - Missing dependency causing stale closures
   - Object recreation in parent component
   - Async operations without cleanup

4. Recommended Fix Pattern:
   ```typescript
   useEffect(() => {
     let cancelled = false;
     
     const fetchData = async () => {
       if (cancelled) return;
       // fetch logic
     };
     
     fetchData();
     
     return () => {
       cancelled = true; // Cleanup
     };
   }, [stableDependencies]); // Use primitive values or refs
   ```

5. Testing After Fix:
   - Add test case that triggers multiple rapid re-renders
   - Monitor re-render count with React DevTools Profiler
   - Verify no memory leaks with heap snapshots
   - Test with React Strict Mode enabled

Success Criteria:
- No infinite loops detected
- Render count stays reasonable (< 5 per user action)
- Memory usage stable over time
- All existing tests still pass
```

---

## Example 3: Performance Request → Measurable Optimization Plan

### Original Request:
```
"Make it load faster"
```

### Context Discovered:
- Next.js 14 application
- Large images on homepage
- No caching strategy
- Lighthouse score: 45/100

### Enhanced Prompt:
```
Optimize homepage performance to achieve Lighthouse score > 90:

Target Page: src/app/page.tsx
Current Score: 45/100 (Performance)

Performance Audit Results:
- Largest Contentful Paint (LCP): 4.2s → Target: < 2.5s
- First Input Delay (FID): 180ms → Target: < 100ms
- Cumulative Layout Shift (CLS): 0.25 → Target: < 0.1

Optimization Checklist:

1. Image Optimization:
   ```tsx
   // Replace <img> with Next.js Image component
   import Image from 'next/image';
   
   <Image
     src="/hero.jpg"
     alt="Hero image"
     width={1200}
     height={600}
     priority // For above-fold images
     placeholder="blur"
     blurDataURL={blurDataUrl}
   />
   ```
   - Convert images to WebP format
   - Implement responsive images with srcSet
   - Add explicit width/height to prevent CLS
   - Use priority loading for hero image

2. Code Splitting:
   ```tsx
   // Lazy load non-critical components
   const HeavyComponent = dynamic(
     () => import('./HeavyComponent'),
     { loading: () => <Skeleton /> }
   );
   ```
   - Split vendor bundles
   - Route-based code splitting
   - Component-level lazy loading

3. Font Optimization:
   ```tsx
   // In layout.tsx
   import { Inter } from 'next/font/google';
   
   const inter = Inter({
     subsets: ['latin'],
     display: 'swap',
     preload: true,
   });
   ```
   - Use next/font for automatic optimization
   - Subset fonts to reduce size
   - Preload critical fonts

4. Caching Strategy:
   ```tsx
   // In page.tsx
   export const revalidate = 3600; // ISR: revalidate every hour
   
   // Or static generation
   export const dynamic = 'force-static';
   ```
   - Implement ISR for dynamic content
   - Add proper Cache-Control headers
   - Use SWR for client-side caching

5. Remove Render-Blocking Resources:
   - Inline critical CSS
   - Defer non-critical JavaScript
   - Remove unused CSS with PurgeCSS

6. Implement Skeleton Screens:
   - Add loading states for async content
   - Prevent layout shift during loading
   - Use React Suspense boundaries

Measurement:
1. Before optimization:
   ```bash
   npm run build
   npm run lighthouse -- --view
   ```

2. After each optimization:
   - Run Lighthouse again
   - Compare bundle size: `npm run analyze`
   - Measure with WebPageTest from multiple locations

3. Monitoring:
   - Set up Core Web Vitals tracking
   - Use Next.js Analytics or Vercel Analytics
   - Track real user metrics (RUM)

Success Criteria:
- Lighthouse Performance score: > 90
- LCP: < 2.5 seconds
- FID: < 100 milliseconds
- CLS: < 0.1
- Bundle size reduction: > 30%
```

---

## Example 4: Simple Refactor → Comprehensive Code Quality Improvement

### Original Request:
```
"Clean up the code"
```

### Context Discovered:
- TypeScript React component
- File: src/components/Dashboard.tsx
- 450 lines, multiple responsibilities
- No tests

### Enhanced Prompt:
```
Refactor Dashboard component following SOLID principles and best practices:

Target: src/components/Dashboard.tsx (450 lines)

Code Quality Issues Identified:
1. Single Responsibility Violation
   - Mixing data fetching, business logic, and presentation
   - Multiple concerns in one component

2. Poor Naming Conventions
   - Generic names: data, info, handleClick
   - Non-descriptive function names

3. No Error Boundaries
   - Unhandled promise rejections
   - Missing loading/error states

4. Prop Drilling
   - Passing props through 4+ levels
   - No context or state management

Refactoring Plan:

Phase 1 - Extract Custom Hooks:
```tsx
// Create src/hooks/useDashboardData.ts
export const useDashboardData = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    fetchDashboardData()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  
  return { data, loading, error, refetch };
};
```

Phase 2 - Split into Smaller Components:
```
src/components/Dashboard/
├── Dashboard.tsx (main container)
├── DashboardHeader.tsx
├── DashboardStats.tsx
├── DashboardChart.tsx
├── DashboardTable.tsx
└── __tests__/
    └── Dashboard.test.tsx
```

Phase 3 - Implement Context for Shared State:
```tsx
// src/contexts/DashboardContext.tsx
const DashboardContext = createContext<DashboardContextValue | null>(null);

export const DashboardProvider: React.FC<Props> = ({ children }) => {
  const dashboardData = useDashboardData();
  return (
    <DashboardContext.Provider value={dashboardData}>
      {children}
    </DashboardContext.Provider>
  );
};
```

Phase 4 - Add TypeScript Strict Types:
```tsx
// src/types/dashboard.ts
export interface DashboardData {
  stats: DashboardStats;
  chartData: ChartDataPoint[];
  tableData: TableRow[];
  lastUpdated: Date;
}

export type DashboardStats = {
  totalUsers: number;
  activeUsers: number;
  revenue: number;
  growth: number;
};
```

Phase 5 - Implement Error Boundaries:
```tsx
// src/components/Dashboard/DashboardErrorBoundary.tsx
class DashboardErrorBoundary extends React.Component<Props, State> {
  // Error boundary implementation
}
```

Phase 6 - Add Unit Tests:
```tsx
// src/components/Dashboard/__tests__/Dashboard.test.tsx
describe('Dashboard', () => {
  it('renders loading state initially', () => {
    // Test loading state
  });
  
  it('renders data after successful fetch', async () => {
    // Test data display
  });
  
  it('renders error state on fetch failure', async () => {
    // Test error handling
  });
});
```

Naming Convention Updates:
- data → dashboardData
- handleClick → handleDashboardRefresh
- info → userStatistics
- comp → chartComponent

Code Style Requirements:
- Max component size: 150 lines
- Max function length: 30 lines
- Use descriptive variable names
- Add JSDoc comments for complex functions
- Use TypeScript strict mode

Success Metrics:
- Component size reduced to < 150 lines each
- Test coverage > 80%
- TypeScript strict mode passing
- ESLint warnings: 0
- No prop drilling beyond 2 levels
- Improved Lighthouse accessibility score
```

---

## Example 5: Database Request → Secure, Efficient Implementation

### Original Request:
```
"Save user data to database"
```

### Context Discovered:
- Express.js + PostgreSQL
- Using Prisma ORM
- User registration endpoint needed
- No validation or security currently

### Enhanced Prompt:
```
Implement secure user registration with database persistence:

Endpoint: POST /api/auth/register
File: src/routes/auth.routes.ts

Data Model (Prisma):
```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String   // Hashed
  firstName String
  lastName  String
  role      Role     @default(USER)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([email])
}

enum Role {
  USER
  ADMIN
}
```

Security Requirements:

1. Input Validation (using Joi):
```typescript
const registerSchema = Joi.object({
  email: Joi.string()
    .email()
    .required()
    .max(255),
  password: Joi.string()
    .min(8)
    .max(100)
    .pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/)
    .required()
    .messages({
      'string.pattern.base': 'Password must contain uppercase, lowercase, number, and special character'
    }),
  firstName: Joi.string()
    .min(1)
    .max(50)
    .required(),
  lastName: Joi.string()
    .min(1)
    .max(50)
    .required()
});
```

2. Password Hashing:
```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;
const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);
```

3. Database Transaction:
```typescript
try {
  const user = await prisma.user.create({
    data: {
      email: email.toLowerCase(), // Normalize email
      password: hashedPassword,
      firstName,
      lastName,
    },
    select: { // Don't return password
      id: true,
      email: true,
      firstName: true,
      lastName: true,
      role: true,
      createdAt: true,
    }
  });
  
  return res.status(201).json({ user });
} catch (error) {
  if (error.code === 'P2002') { // Unique constraint violation
    return res.status(409).json({ 
      error: 'Email already registered' 
    });
  }
  throw error; // Let error handler catch others
}
```

4. Rate Limiting:
```typescript
import rateLimit from 'express-rate-limit';

const registerLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
  message: 'Too many registration attempts, please try again later'
});

router.post('/register', registerLimiter, registerController);
```

5. Email Verification (Optional):
```typescript
// Generate verification token
const verificationToken = crypto.randomBytes(32).toString('hex');

await prisma.user.update({
  where: { id: user.id },
  data: {
    verificationToken,
    verificationTokenExpiry: new Date(Date.now() + 24 * 60 * 60 * 1000)
  }
});

// Send verification email
await sendVerificationEmail(user.email, verificationToken);
```

Error Handling:
```typescript
// In middleware/errorHandler.ts
export const errorHandler = (err, req, res, next) => {
  if (err instanceof ValidationError) {
    return res.status(400).json({ 
      error: 'Validation failed', 
      details: err.details 
    });
  }
  
  if (err instanceof PrismaClientKnownRequestError) {
    return res.status(500).json({ 
      error: 'Database error' 
    });
  }
  
  // Don't leak error details in production
  const message = process.env.NODE_ENV === 'production' 
    ? 'Internal server error' 
    : err.message;
    
  res.status(500).json({ error: message });
};
```

Logging:
```typescript
import winston from 'winston';

logger.info('User registration attempt', { email });
logger.info('User registered successfully', { userId: user.id });
logger.error('Registration failed', { error: err.message, email });
```

Testing Checklist:
- [ ] Valid registration succeeds
- [ ] Duplicate email returns 409
- [ ] Invalid email format returns 400
- [ ] Weak password rejected
- [ ] Rate limiting works after 5 attempts
- [ ] Password is hashed in database
- [ ] Verification email sent
- [ ] No password in response

Security Checklist:
- [ ] HTTPS only in production
- [ ] CORS configured properly
- [ ] Helmet.js security headers
- [ ] SQL injection prevented (Prisma handles this)
- [ ] XSS prevention (sanitize inputs)
- [ ] CSRF tokens for session-based auth
- [ ] Audit log for registrations
```

---

## Common Enhancement Patterns

### Pattern 1: "Make it work" → "Make it production-ready"
Add:
- Error handling
- Input validation
- Logging
- Tests
- Documentation
- Security checks

### Pattern 2: "Add feature X" → "Add feature X with Y constraints"
Specify:
- Performance requirements
- Browser/device compatibility
- Accessibility standards
- Internationalization
- Mobile responsiveness

### Pattern 3: "Fix bug" → "Root cause analysis and fix"
Include:
- Reproduction steps
- Error logs/stack traces
- Expected vs actual behavior
- Proposed solution with reasoning
- Test cases to prevent regression

### Pattern 4: "Implement design" → "Implement design with specs"
Detail:
- Exact spacing (px/rem)
- Color codes (hex/rgb)
- Font sizes and weights
- Breakpoints for responsive
- Animation timings
- Hover/focus states

---

## User Feedback Loop

After presenting an enhanced prompt:

1. **Confirmation**: "Does this match your intent?"
2. **Adjustment**: "Would you like to add/remove any requirements?"
3. **Clarification**: "Are there any constraints I should know about?"
4. **Prioritization**: "Which aspects are most critical?"

Then proceed with implementation only after approval.
