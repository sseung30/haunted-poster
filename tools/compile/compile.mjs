// Compile poster images into targets.mind, same as the MindAR web compiler.
// Usage: node compile.mjs <out.mind> <image1.png> [image2.png ...]
import { writeFileSync } from "node:fs";
import { loadImage } from "canvas";
import * as tf from "@tensorflow/tfjs";
import { OfflineCompiler } from "mind-ar/src/image-target/offline-compiler.js";

const [out, ...inputs] = process.argv.slice(2);
if (!out || inputs.length === 0) {
  console.error("usage: node compile.mjs <out.mind> <image...>");
  process.exit(1);
}

await tf.setBackend("cpu");
const images = await Promise.all(inputs.map((p) => loadImage(p)));
const compiler = new OfflineCompiler();
let last = -10;
await compiler.compileImageTargets(images, (p) => {
  if (p - last >= 10) { console.log(`compiling... ${Math.floor(p)}%`); last = p; }
});
writeFileSync(out, Buffer.from(compiler.exportData()));
console.log("wrote", out);
