import {defineConfig} from 'vite';
import motionCanvasExport from '@motion-canvas/vite-plugin';
import ffmpegExport from '@motion-canvas/ffmpeg';

// Vite's CJS/ESM interop may wrap these plugins in a second .default on Linux.
const unwrap = (entry: any) => typeof entry === 'function' ? entry : (entry?.default ?? entry);
const motionCanvas = unwrap(motionCanvasExport);
const ffmpeg = unwrap(ffmpegExport);
if (typeof motionCanvas !== 'function' || typeof ffmpeg !== 'function') {
  throw new Error('Motion Canvas Vite plugin export cannot be resolved');
}
export default defineConfig({plugins:[...motionCanvas(),ffmpeg()],server:{port:9000}});
