import { FileBlob, PresentationFile } from "@oai/artifact-tool";
const source = "D:\\SIH2026-IDEA-Presentation-Format.pptx";
const p = await PresentationFile.importPptx(await FileBlob.load(source));
const result = await p.inspect({ kind: "slide,textbox,shape,image,table,chart,notes,layout", maxChars: 30000 });
console.log(result.ndjson);
