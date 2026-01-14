# Station 4.1 - SvelteKit Frontend Setup

## Overview
Initialize SvelteKit project with TypeScript, Tailwind CSS, and atomic-era theme configuration. Set up the foundation for the Atomic Cat AI frontend.

## Learning Objectives
- Bootstrap SvelteKit project with proper configuration
- Configure Tailwind CSS with custom theme
- Set up TypeScript for type safety
- Structure frontend application properly
- Apply atomic-era design tokens

---

## 🎯 GENERATION PROMPT

Create SvelteKit frontend setup for Atomic Cat AI with atomic-era theming:

**Initialize Project:**
```bash
npm create svelte@latest frontend
# Select: Skeleton project, TypeScript, ESLint, Prettier

cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npm install -D @tailwindcss/forms
npx tailwindcss init -p
```

**File: frontend/tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        // Atomic Era Theme
        atomic: {
          teal: '#40E0D0',
          coral: '#FF6F61',
          mustard: '#FFD700',
          mint: '#98FF98',
          cream: '#FFFDD0',
          charcoal: '#36454F',
        }
      },
      fontFamily: {
        display: ['Pacifico', 'cursive'],
        body: ['Quicksand', 'sans-serif'],
      },
      borderRadius: {
        'atomic': '24px',
      },
      boxShadow: {
        'atomic': '4px 4px 0 #36454F',
        'atomic-glow': '0 0 20px rgba(64, 224, 208, 0.3)',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

**File: frontend/src/app.css**
```css
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-body bg-atomic-cream text-atomic-charcoal;
  }
  
  h1, h2, h3, h4, h5, h6 {
    @apply font-display;
  }
}

@layer components {
  .btn-primary {
    @apply bg-atomic-teal text-atomic-charcoal font-semibold py-3 px-6 rounded-atomic;
    @apply hover:bg-atomic-coral hover:shadow-atomic-glow;
    @apply transition-all duration-300;
    @apply active:translate-y-0.5;
  }
  
  .btn-secondary {
    @apply bg-atomic-coral text-white font-semibold py-3 px-6 rounded-atomic;
    @apply hover:bg-atomic-mustard hover:text-atomic-charcoal;
    @apply transition-all duration-300;
  }
  
  .card {
    @apply bg-white border-2 border-atomic-charcoal rounded-2xl p-6;
    @apply shadow-atomic;
  }
  
  .input-atomic {
    @apply bg-white border-2 border-atomic-charcoal rounded-xl px-4 py-3;
    @apply font-body;
    @apply focus:outline-none focus:border-atomic-teal focus:ring-4 focus:ring-atomic-teal/20;
    @apply transition-all duration-300;
  }
}

/* Atomic decorations */
.starburst {
  position: relative;
}

.starburst::before {
  content: "★";
  position: absolute;
  color: var(--tw-atomic-mustard);
  animation: twinkle 2s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background: #FFFDD0;
}

::-webkit-scrollbar-thumb {
  background: #40E0D0;
  border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
  background: #FF6F61;
}
```

**File: frontend/src/app.html**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%sveltekit.assets%/favicon.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Atomic Cat AI - Retro-futuristic AI voice assistant" />
    %sveltekit.head%
  </head>
  <body data-sveltekit-preload-data="hover">
    <div style="display: contents">%sveltekit.body%</div>
  </body>
</html>
```

**File: frontend/vite.config.ts**
```typescript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    port: 5173,
    host: '0.0.0.0',
  },
});
```

**File: frontend/svelte.config.js**
```javascript
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  
  kit: {
    adapter: adapter()
  }
};

export default config;
```

**File: frontend/Dockerfile**
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Production image
FROM node:20-alpine

WORKDIR /app

# Copy built app
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./

# Install production dependencies only
RUN npm ci --production

EXPOSE 5173

CMD ["node", "build"]
```

**File: frontend/.dockerignore**
```
node_modules
.svelte-kit
build
.git
.env
*.log
```

**Requirements**:
1. TypeScript for type safety
2. Tailwind CSS with atomic theme colors
3. Custom fonts: Pacifico (display), Quicksand (body)
4. Atomic design components (buttons, cards, inputs)
5. Proper SvelteKit configuration
6. Docker support for production
7. Custom scrollbar styling
8. Animations respect prefers-reduced-motion

**Output**: Complete SvelteKit project setup with atomic theming.

---

## ✅ VALIDATION PROMPT

Validate SvelteKit frontend setup:

### Project Structure
- [ ] `frontend/` directory exists
- [ ] `package.json` has SvelteKit dependencies
- [ ] `svelte.config.js` configured with node adapter
- [ ] `vite.config.ts` configured
- [ ] `tailwind.config.js` with atomic theme
- [ ] `src/app.css` with custom styles
- [ ] `src/app.html` template
- [ ] `Dockerfile` for production
- [ ] `.dockerignore` excludes node_modules

### Tailwind Configuration
- [ ] Atomic color palette defined:
  - teal: #40E0D0
  - coral: #FF6F61
  - mustard: #FFD700
  - mint: #98FF98
  - cream: #FFFDD0
  - charcoal: #36454F
- [ ] Custom fonts configured (Pacifico, Quicksand)
- [ ] Custom border radius (`atomic`: 24px)
- [ ] Custom shadows (`atomic`, `atomic-glow`)
- [ ] @tailwindcss/forms plugin installed

### Global Styles
- [ ] Google Fonts imported (Pacifico, Quicksand)
- [ ] Body uses Quicksand font and cream background
- [ ] Headings use Pacifico font
- [ ] `.btn-primary` component style defined
- [ ] `.btn-secondary` component style defined
- [ ] `.card` component style defined
- [ ] `.input-atomic` component style defined
- [ ] Custom scrollbar styled with atomic colors
- [ ] Smooth scrolling enabled

### Component Styles
**Button Primary**:
- [ ] Teal background
- [ ] Rounded (24px)
- [ ] Hover: coral background with glow
- [ ] Smooth transitions (300ms)
- [ ] Active state (translate down)

**Card**:
- [ ] White background
- [ ] 2px charcoal border
- [ ] Atomic shadow (4px 4px 0 charcoal)
- [ ] Rounded corners

**Input**:
- [ ] White background
- [ ] Charcoal border
- [ ] Focus: teal border with ring
- [ ] Rounded corners

### Commands to Run
```bash
cd frontend

# Install dependencies
npm install

# Should complete without errors

# Run dev server
npm run dev

# Should start on port 5173

# Build for production
npm run build

# Should create build/ directory

# Run production build
node build

# Should serve on configured port

# Check Tailwind classes work
echo '<button class="btn-primary">Test</button>' > src/routes/+page.svelte
npm run dev
# Visit http://localhost:5173 - button should be styled

# Build Docker image
docker build -t atomic-cat-frontend:test .

# Should complete without errors
```

### Expected Results
- Development server runs on port 5173
- Tailwind CSS compiles correctly
- Atomic theme colors available
- Custom fonts load properly
- Component styles apply correctly
- Production build succeeds
- Docker image builds successfully
- Ready for component development in next stations

---

## Notes
- SvelteKit uses file-based routing (routes in `src/routes/`)
- Atomic theme can be extended in `tailwind.config.js`
- Consider adding more utility classes as needed
- Next stations will build components using these styles
- Keep atomic aesthetic consistent across all components
