import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const base = "C:\\Users\\Gaming\\.gemini\\antigravity\\scratch\\capacity-connect";
const source = path.join(base, "output", "presentations", "capacity-connect-sih-2025-final.pptx");
const out = path.join(base, ".codex-build", "capacity-connect-ppt", "rendered");
await fs.mkdir(out, { recursive: true });
const presentation = await PresentationFile.importPptx(await FileBlob.load(source));
for (let i = 0; i < presentation.slides.items.length; i++) {
  const blob = await presentation.export({ slide: presentation.slides.items[i], format: "png", scale: 1.5 });
  await fs.writeFile(path.join(out, `slide-${i + 1}.png`), new Uint8Array(await blob.arrayBuffer()));
}
console.log(out);
