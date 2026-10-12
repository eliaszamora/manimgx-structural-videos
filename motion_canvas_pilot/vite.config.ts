import {defineConfig} from 'vite';
import motionCanvasModule from '@motion-canvas/vite-plugin';

// The published 3.17.2 package uses a CJS entry point. Vite's config loader
// can expose the default function behind a second '.default' wrapper.
const candidate: any = motionCanvasModule as any;
const motionCanvas = typeof candidate === 'function'
  ? candidate
  : typeof candidate?.default === 'function'
    ? candidate.default
    : candidate?.default?.default;
if (typeof motionCanvas !== 'function') {
  throw new Error('Motion Canvas Vite factory export could not be resolved');
}
export default defineConfig({plugins:[motionCanvas({project:'./src/project.ts'})]});
