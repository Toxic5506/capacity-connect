import { FileBlob, PresentationFile } from "@oai/artifact-tool";
const p = await PresentationFile.importPptx(await FileBlob.load("D:\\SIH2026-IDEA-Presentation-Format.pptx"));
console.log("slides", Object.getOwnPropertyNames(Object.getPrototypeOf(p.slides)));
console.log("items", p.slides.items.length, Object.getOwnPropertyNames(Object.getPrototypeOf(p.slides.items)));
console.log("last", Object.getOwnPropertyNames(Object.getPrototypeOf(p.slides.items[6])));
console.log("remove", p.slides.remove.toString());
console.log("delete", p.slides.items[6].delete.toString());
