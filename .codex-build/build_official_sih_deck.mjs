import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "C:\\Users\\Gaming\\.gemini\\antigravity\\scratch\\capacity-connect";
const skillDir = "C:\\Users\\Gaming\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.905.11957\\skills\\presentations";
const sourceTemplatePath = "D:\\SIH2026-IDEA-Presentation-Format.pptx";
const buildDir = path.join(workspaceDir, ".codex-build", "official-sih-deck");
const finalPath = path.join(workspaceDir, "output", "presentations", "capacity-connect-official-sih-2026.pptx");
const candidatePath = path.join(buildDir, "candidate.pptx");
const runtimePython = "C:\\Users\\Gaming\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, "container_tools", "artifact_tool_utils.mjs")).href);

await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });
const p = await PresentationFile.importPptx(await FileBlob.load(sourceTemplatePath));

function replace(id, before, after) {
  const target = p.resolve(id);
  target.text.replace(before, after);
}

// Preserve the template's six intended slides and delete the instruction page.
p.slides.remove(p.slides.getItem(6));

// Slide 1: title-page fields
replace("sh/wn6dc7eh", "\nProblem Statement ID –\nProblem Statement Title-\nTheme-\nPS Category- Software/Hardware\nTeam ID-\nTeam Name (Registered on portal)", `\nProblem Statement ID - 26075\nProblem Statement Title - CAPACITY CONNECT A Digital Capacity Building and Learning Management Portal\nTheme - Smart Education\nPS Category - Software\nTeam ID -\nTeam Name - byte force`);

// Slide 2: idea title and concise solution points
replace("sh/dkvmpszm", "\nIDEA TITLE", "\nCAPACITY CONNECT");
replace("sh/qx4nud0b", "Proposed Solution (Describe your Idea/Solution/Prototype)\n\n\nDetailed explanation of the proposed solution\n How it addresses the problem\nInnovation and uniqueness of the solution ", `Proposed Solution\n\n• A role-based digital portal for trainees, trainers, and administrators.\n• Centralises courses, learning resources, enrolments, assessments, certificates, and competency records.\n• Replaces fragmented trackers with one searchable learning and capacity-building workflow.\n\nHow it addresses the problem\n• Administrators approve users, assign roles, publish announcements, and monitor activity.\n• Trainees enrol, learn, attempt timed MCQ assessments, and receive certificates after passing.\n\nInnovation and uniqueness\n• Connects learner progress, trainer expertise, competency mapping, and certificates in one lightweight portal.`);
replace("sh/ove9o7yd", "Your Team Name", "byte force");

// Slide 3: technical approach
replace("sh/1k3214v2", "Technologies to be used (e.g. programming languages, frameworks, hardware)\nMethodology and process for implementation (Flow Charts/Images/ working prototype)", `Technologies used\n• Python, Flask, Jinja templates, Flask-SQLAlchemy, SQLAlchemy, SQLite, Werkzeug\n• Tailwind CSS, Lucide icons, Chart.js, Google Fonts\n• Local static storage for resources and uploaded certificates\n\nImplementation flow\n• Registration and administrator approval → role-based dashboard\n• Course enrolment → resource access → timed assessment\n• Score calculation → certificate creation → enrolment progress update\n• Competency mapping links trainers with course subject areas\n\nPrototype status\n• Functional local web prototype with core LMS workflows implemented.`);
replace("sh/m1c3mlsn", "Your Team Name", "byte force");

// Slide 4: feasibility and viability
replace("sh/sjad83id", "Analysis of the feasibility of the idea\nPotential challenges and risks\nStrategies for overcoming these challenges", `Feasibility\n• The working prototype already supports accounts, approvals, courses, resources, assessments, certificates, and competency mapping.\n• Flask and SQLite enable a low-cost local pilot with minimal infrastructure.\n• The data model can move to a managed database as adoption grows.\n\nChallenges and risks\n• Demo authentication must be removed before production use.\n• Upload validation, CSRF protection, audit logs, backups, and secure secret management are required.\n• Local SQLite and file storage do not suit multi-server scale.\n\nStrategy\n• Pilot with a focused learner cohort, then move to production Flask, PostgreSQL, and managed object storage.`);
replace("sh/i94r6xgz", "Your Team Name", "byte force");

// Slide 5: impact and benefits
replace("sh/g7alsnu1", "Potential impact on the target audience\nBenefits of the solution (social, economic, environmental, etc.)", `Impact on target users\n• Trainees follow a visible path from enrolment to assessment and certification.\n• Trainers publish resources, create questionnaires, and review learner performance.\n• Administrators manage approvals, roles, announcements, and dashboard metrics.\n• Programme managers identify trainer capability through competency mapping.\n\nBenefits\n• A central course and resource library reduces duplicate sharing and manual tracking.\n• Unique certificate codes provide a verifiable learning record.\n• Feedback and assessment outcomes support content improvement.\n• The platform supports repeatable capacity-building programmes across subject areas.`);
replace("sh/ahkvi1cb", "Your Team Name", "byte force");

// Slide 6: research and references
replace("sh/vq5cve1s", "Details / Links of the reference and research work", `Prototype reference\n• Capacity Connect source review: app.py, models.py, config.py, routes/, templates/, and requirements.txt.\n• Functional review confirms Flask server rendering, SQLAlchemy data models, SQLite storage, local uploads, assessments, certificates, and role-based workflows.\n\nOfficial format reference\n• Smart India Hackathon 2026 Idea Presentation Format supplied by SIH.\n\nPilot research plan\n• Test representative trainee, trainer, and administrator workflows.\n• Measure enrolment completion, assessment completion, certificate issuance, and user feedback.\n• Document privacy, retention, access-control, backup, and governance requirements before deployment.`);
replace("sh/pc76hkr2", "Your Team Name", "byte force");

await (await PresentationFile.exportPptx(p)).save(candidatePath);
const result = await finalizePresentation({
  explicitTotalSlideCount: 6,
  sourceTemplatePath,
  requiredTemplateReferenceSlides: [1, 2, 3, 4, 5, 6],
  minimumTemplateCoverageRatio: 1,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-bullet-geometry", "--validate-heading-fit"],
  verifyArtifactToolImport: true,
  receiptPath: path.join(buildDir, "validation.json"),
});
console.log(JSON.stringify({ finalPath, result }, null, 2));
