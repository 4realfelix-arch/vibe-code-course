# Station 4.6 - Animated Cat Avatar

## Overview
Create the iconic Atomic Cat avatar - a 1940s-style black cat SVG with animated states (idle, listening, thinking, speaking, happy, error). Features yellow almond eyes, coral choker with gem, and smooth CSS animations.

## Learning Objectives
- Build SVG graphics with proper structure
- Implement CSS keyframe animations
- Handle animation state changes in Svelte
- Apply atomic-era design aesthetic
- Create accessible, performant animations

---

## 🎯 GENERATION PROMPT

Create the Atomic Cat avatar component for Atomic Cat AI with these exact specifications:

**File: frontend/src/lib/components/CatAvatar.svelte**

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  
  export let state: 'idle' | 'listening' | 'thinking' | 'speaking' | 'happy' | 'error' = 'idle';
  export let size: number = 200;
  
  // Animation state tracking
  let currentState = state;
  $: currentState = state;
</script>

<div class="cat-avatar" style="width: {size}px; height: {size}px;">
  <svg
    viewBox="0 0 200 240"
    xmlns="http://www.w3.org/2000/svg"
    class="cat-svg"
    class:idle={currentState === 'idle'}
    class:listening={currentState === 'listening'}
    class:thinking={currentState === 'thinking'}
    class:speaking={currentState === 'speaking'}
    class:happy={currentState === 'happy'}
    class:error={currentState === 'error'}
  >
    <!-- Cat body -->
    <g id="cat-body">
      <!-- Main body (skinny, elegant) -->
      <ellipse
        cx="100"
        cy="140"
        rx="35"
        ry="60"
        fill="#000000"
        class="body"
      />
      
      <!-- Head -->
      <ellipse
        cx="100"
        cy="80"
        rx="45"
        ry="50"
        fill="#000000"
        class="head"
      />
      
      <!-- Left ear -->
      <polygon
        points="70,50 60,20 80,45"
        fill="#000000"
        class="ear-left"
      />
      
      <!-- Right ear -->
      <polygon
        points="130,50 140,20 120,45"
        fill="#000000"
        class="ear-right"
      />
      
      <!-- Inner ear details -->
      <polygon
        points="72,48 66,30 78,46"
        fill="#FF6F61"
        opacity="0.6"
      />
      <polygon
        points="128,48 134,30 122,46"
        fill="#FF6F61"
        opacity="0.6"
      />
    </g>
    
    <!-- Eyes (yellow almond-shaped) -->
    <g id="eyes" class="eyes">
      <!-- Left eye -->
      <ellipse
        cx="85"
        cy="75"
        rx="12"
        ry="16"
        fill="#FFD700"
        class="eye-left"
      />
      <!-- Left pupil -->
      <ellipse
        cx="85"
        cy="75"
        rx="5"
        ry="8"
        fill="#000000"
        class="pupil-left"
      />
      
      <!-- Right eye -->
      <ellipse
        cx="115"
        cy="75"
        rx="12"
        ry="16"
        fill="#FFD700"
        class="eye-right"
      />
      <!-- Right pupil -->
      <ellipse
        cx="115"
        cy="75"
        rx="5"
        ry="8"
        fill="#000000"
        class="pupil-right"
      />
    </g>
    
    <!-- Nose -->
    <path
      d="M 100 88 L 95 95 L 105 95 Z"
      fill="#FF6F61"
      class="nose"
    />
    
    <!-- Mouth -->
    <g id="mouth" class="mouth">
      <path
        d="M 100 95 Q 95 100 90 98"
        stroke="#000000"
        stroke-width="2"
        fill="none"
        class="mouth-left"
      />
      <path
        d="M 100 95 Q 105 100 110 98"
        stroke="#000000"
        stroke-width="2"
        fill="none"
        class="mouth-right"
      />
    </g>
    
    <!-- Whiskers -->
    <g id="whiskers" class="whiskers">
      <line x1="50" y1="80" x2="20" y2="75" stroke="#000000" stroke-width="1.5" />
      <line x1="50" y1="85" x2="20" y2="85" stroke="#000000" stroke-width="1.5" />
      <line x1="50" y1="90" x2="20" y2="95" stroke="#000000" stroke-width="1.5" />
      
      <line x1="150" y1="80" x2="180" y2="75" stroke="#000000" stroke-width="1.5" />
      <line x1="150" y1="85" x2="180" y2="85" stroke="#000000" stroke-width="1.5" />
      <line x1="150" y1="90" x2="180" y2="95" stroke="#000000" stroke-width="1.5" />
    </g>
    
    <!-- Coral choker with gem -->
    <g id="choker">
      <ellipse
        cx="100"
        cy="115"
        rx="28"
        ry="8"
        fill="none"
        stroke="#FF6F61"
        stroke-width="4"
        class="choker-band"
      />
      
      <!-- Gem -->
      <circle
        cx="100"
        cy="115"
        r="6"
        fill="#40E0D0"
        class="gem"
      />
      <circle
        cx="100"
        cy="115"
        r="3"
        fill="#FFFFFF"
        opacity="0.7"
        class="gem-highlight"
      />
    </g>
    
    <!-- Tail (curved) -->
    <path
      d="M 130 160 Q 160 180 155 220 Q 150 240 140 235"
      stroke="#000000"
      stroke-width="12"
      fill="none"
      stroke-linecap="round"
      class="tail"
    />
  </svg>
</div>

<style lang="scss">
  .cat-avatar {
    display: inline-block;
    position: relative;
  }
  
  .cat-svg {
    width: 100%;
    height: 100%;
  }
  
  /* Animation: Idle - gentle tail swish and blink */
  .cat-svg.idle {
    .tail {
      animation: tail-swish 3s ease-in-out infinite;
    }
    
    .eyes {
      animation: blink 4s ease-in-out infinite;
    }
  }
  
  @keyframes tail-swish {
    0%, 100% {
      transform: rotate(0deg);
      transform-origin: 130px 160px;
    }
    50% {
      transform: rotate(-8deg);
      transform-origin: 130px 160px;
    }
  }
  
  @keyframes blink {
    0%, 45%, 55%, 100% {
      transform: scaleY(1);
    }
    50% {
      transform: scaleY(0.1);
    }
  }
  
  /* Animation: Listening - ears perk up */
  .cat-svg.listening {
    .ear-left {
      animation: perk-left 0.3s ease-out forwards;
    }
    
    .ear-right {
      animation: perk-right 0.3s ease-out forwards;
    }
    
    .eyes {
      transform: scale(1.1);
      transition: transform 0.3s ease;
    }
  }
  
  @keyframes perk-left {
    from {
      transform: rotate(0deg);
      transform-origin: 70px 50px;
    }
    to {
      transform: rotate(-10deg);
      transform-origin: 70px 50px;
    }
  }
  
  @keyframes perk-right {
    from {
      transform: rotate(0deg);
      transform-origin: 130px 50px;
    }
    to {
      transform: rotate(10deg);
      transform-origin: 130px 50px;
    }
  }
  
  /* Animation: Thinking - eyes look up */
  .cat-svg.thinking {
    .pupil-left, .pupil-right {
      animation: look-up 2s ease-in-out infinite;
    }
    
    .tail {
      animation: tail-twitch 1s ease-in-out infinite;
    }
  }
  
  @keyframes look-up {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-5px);
    }
  }
  
  @keyframes tail-twitch {
    0%, 100% {
      transform: rotate(0deg);
      transform-origin: 130px 160px;
    }
    50% {
      transform: rotate(-15deg);
      transform-origin: 130px 160px;
    }
  }
  
  /* Animation: Speaking - mouth moves */
  .cat-svg.speaking {
    .mouth {
      animation: mouth-move 0.3s ease-in-out infinite;
    }
    
    .choker-band {
      animation: vibrate 0.3s ease-in-out infinite;
    }
  }
  
  @keyframes mouth-move {
    0%, 100% {
      transform: scaleY(1);
    }
    50% {
      transform: scaleY(1.3);
    }
  }
  
  @keyframes vibrate {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(2px);
    }
  }
  
  /* Animation: Happy - eyes become crescents */
  .cat-svg.happy {
    .eye-left, .eye-right {
      animation: squint 0.5s ease-out forwards;
    }
    
    .mouth {
      animation: smile 0.5s ease-out forwards;
    }
    
    .tail {
      animation: tail-wag 0.6s ease-in-out 3;
    }
  }
  
  @keyframes squint {
    to {
      transform: scaleY(0.3);
    }
  }
  
  @keyframes smile {
    to {
      transform: translateY(5px) scale(1.2);
    }
  }
  
  @keyframes tail-wag {
    0%, 100% {
      transform: rotate(0deg);
      transform-origin: 130px 160px;
    }
    25% {
      transform: rotate(-20deg);
      transform-origin: 130px 160px;
    }
    75% {
      transform: rotate(20deg);
      transform-origin: 130px 160px;
    }
  }
  
  /* Animation: Error - ears flat */
  .cat-svg.error {
    .ear-left {
      animation: flatten-left 0.3s ease-out forwards;
    }
    
    .ear-right {
      animation: flatten-right 0.3s ease-out forwards;
    }
    
    .body {
      animation: shake 0.5s ease-in-out 2;
    }
  }
  
  @keyframes flatten-left {
    to {
      transform: rotate(45deg);
      transform-origin: 70px 50px;
    }
  }
  
  @keyframes flatten-right {
    to {
      transform: rotate(-45deg);
      transform-origin: 130px 50px;
    }
  }
  
  @keyframes shake {
    0%, 100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-3px);
    }
    75% {
      transform: translateX(3px);
    }
  }
  
  /* Accessibility: Respect reduced motion preference */
  @media (prefers-reduced-motion: reduce) {
    .cat-svg * {
      animation: none !important;
      transition: none !important;
    }
  }
  
  /* Add subtle glow to gem */
  .gem {
    filter: drop-shadow(0 0 3px #40E0D0);
  }
  
  /* Smooth state transitions */
  .cat-svg * {
    transition: transform 0.3s ease, opacity 0.3s ease;
  }
</style>
```

**Requirements**:
1. Exact SVG structure as specified:
   - Skinny, elegant black cat body
   - Yellow almond eyes (#FFD700)
   - Coral choker (#FF6F61) with teal gem (#40E0D0)
   - Pointed ears with coral inner details
   - Curved tail
   - Whiskers extending from face
2. Six animation states:
   - **idle**: Tail swish (3s cycle), occasional blink (4s cycle)
   - **listening**: Ears perk up, eyes widen
   - **thinking**: Eyes look up, tail twitches
   - **speaking**: Mouth moves, choker vibrates slightly
   - **happy**: Eyes squint to crescents, mouth smiles, tail wags energetically
   - **error**: Ears flatten, body shakes
3. All animations use CSS `@keyframes`
4. State transitions are smooth (300ms ease)
5. Respects `prefers-reduced-motion` accessibility setting
6. Gem has subtle glow effect
7. Proper transform origins for natural rotations

**Output**: Complete, animated cat avatar component.

---

## ✅ VALIDATION PROMPT

Validate the cat avatar implementation:

### SVG Structure
- [ ] **Body**: Skinny ellipse (35x60), black, centered
- [ ] **Head**: Ellipse (45x50), black, above body
- [ ] **Ears**: Two triangular polygons, pointed upward
- [ ] **Inner ears**: Coral-colored triangles inside ears
- [ ] **Eyes**: Two yellow (#FFD700) almond ellipses with black pupils
- [ ] **Nose**: Pink triangle (#FF6F61)
- [ ] **Mouth**: Two curved paths forming smile
- [ ] **Whiskers**: 6 lines (3 each side)
- [ ] **Choker**: Coral (#FF6F61) ellipse around neck
- [ ] **Gem**: Teal (#40E0D0) circle on choker with white highlight
- [ ] **Tail**: Curved path, rounded ends

### Animation States

**Idle**:
- [ ] Tail swishes side to side (3s cycle)
- [ ] Eyes blink occasionally (4s cycle)
- [ ] Gentle, relaxed movements

**Listening**:
- [ ] Ears rotate outward (perk up)
- [ ] Eyes scale up 10%
- [ ] Animation completes in 300ms

**Thinking**:
- [ ] Pupils move up and down (2s cycle)
- [ ] Tail twitches (1s cycle)
- [ ] Contemplative feel

**Speaking**:
- [ ] Mouth scales vertically (300ms cycle)
- [ ] Choker vibrates slightly
- [ ] Rapid, energetic movement

**Happy**:
- [ ] Eyes squint to 30% height (crescent eyes)
- [ ] Mouth enlarges and moves down
- [ ] Tail wags side to side vigorously (3 wags)
- [ ] Joyful, expressive

**Error**:
- [ ] Ears flatten (rotate 45° toward head)
- [ ] Body shakes horizontally (2 shakes)
- [ ] Distressed appearance

### CSS Animations
- [ ] All animations use `@keyframes`
- [ ] Transform origins set correctly for natural rotation
- [ ] Smooth transitions (300ms ease) between states
- [ ] Animations loop appropriately (infinite for idle, thinking, speaking)
- [ ] One-time animations complete properly (listening, happy, error)

### Accessibility
- [ ] `@media (prefers-reduced-motion: reduce)` disables all animations
- [ ] Component remains usable without animations
- [ ] No flashing or seizure-inducing effects

### Component Props
- [ ] `state` prop accepts all six state values
- [ ] `size` prop scales entire avatar proportionally
- [ ] Default size is 200px
- [ ] State changes trigger smooth transitions

### Visual Quality
- [ ] SVG scales cleanly at any size
- [ ] Colors match atomic theme (teal, coral, mustard)
- [ ] Gem has subtle glow effect (drop-shadow)
- [ ] No pixelation or artifacts
- [ ] Silhouette is recognizable as a cat

### Commands to Test
```html
<!-- Test in frontend/src/routes/+page.svelte -->
<script>
  import CatAvatar from '$lib/components/CatAvatar.svelte';
  import { writable } from 'svelte/store';
  
  let state = writable('idle');
  let currentState = 'idle';
  
  const states = ['idle', 'listening', 'thinking', 'speaking', 'happy', 'error'];
  let stateIndex = 0;
  
  function cycleState() {
    stateIndex = (stateIndex + 1) % states.length;
    currentState = states[stateIndex];
  }
  
  // Auto-cycle every 3 seconds
  setInterval(cycleState, 3000);
</script>

<div style="text-align: center; padding: 50px;">
  <h1>Atomic Cat Avatar Test</h1>
  
  <CatAvatar state={currentState} size={300} />
  
  <p>Current state: <strong>{currentState}</strong></p>
  
  <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px;">
    {#each states as s}
      <button on:click={() => currentState = s}>
        {s}
      </button>
    {/each}
  </div>
</div>
```

### Expected Results
- Avatar renders with correct proportions
- All six states display unique animations
- Transitions between states are smooth
- Colors match atomic theme exactly
- Avatar is visually appealing and recognizable
- Animations enhance personality without being distracting
- No performance issues (60fps)

---

## Notes
- This is the visual identity of Atomic Cat AI - make it memorable!
- SVG paths may need tweaking for perfect cat shape
- Consider adding more subtle animations (ear twitches, whisker trembles)
- Gem could pulse during "thinking" state
- Test on different screen sizes
- Consider adding sound effects in future (purr, meow)
- This component will be used in main layout (station 4.4)
