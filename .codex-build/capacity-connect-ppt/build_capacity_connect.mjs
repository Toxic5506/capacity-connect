import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const skillDir = "C:\\Users\\Gaming\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.905.11957\\skills\\presentations";
const workspaceDir = "C:\\Users\\Gaming\\.gemini\\antigravity\\scratch\\capacity-connect";
const buildDir = path.join(workspaceDir, ".codex-build", "capacity-connect-ppt");
const outputDir = path.join(workspaceDir, "output", "presentations");
const candidatePath = path.join(buildDir, "capacity-connect-candidate.pptx");
const finalPath = path.join(outputDir, "capacity-connect-sih-2025-final.pptx");
const runtimePython = "C:\\Users\\Gaming\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";

const { resolvePresentationFont, finalizePresentation } = await import(pathToFileURL(
  path.join(skillDir, "container_tools", "artifact_tool_utils.mjs")).href);
const font = resolvePresentationFont();
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });

const ppt = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const blue = "#0B75BD";
const darkBlue = "#234F86";
const navy = "#183A68";
const black = "#111111";
const lightBlue = "#E9F4FC";
const paleGreen = "#EAF7F2";
const paleGold = "#FFF4D7";
const white = "#FFFFFF";
const gray = "#D9E2EA";

function box(slide, left, top, width, height, fill = "none", line = "none", radius = false) {
  return slide.shapes.add({
    geometry: radius ? "roundRect" : "rect",
    position: { left, top, width, height },
    fill,
    line: { fill: line, width: line === "none" ? 0 : 1 },
  });
}
function text(slide, value, left, top, width, height, opts = {}) {
  const shape = box(slide, left, top, width, height, "none", "none");
  shape.text = value;
  shape.text.style = {
    typeface: opts.font || font,
    fontSize: opts.size || 20,
    bold: opts.bold || false,
    italic: opts.italic || false,
    color: opts.color || black,
    align: opts.align || "left",
    verticalAlign: opts.verticalAlign || "top",
    autoFit: "shrinkText",
    breakLine: false,
    marginLeft: opts.margin || 0,
    marginRight: opts.margin || 0,
    marginTop: opts.margin || 0,
    marginBottom: opts.margin || 0,
  };
  return shape;
}
function line(slide, x1, y1, x2, y2, color = blue, width = 1, dash = "solid") {
  if (y1 === y2) return box(slide, Math.min(x1, x2), y1, Math.abs(x2 - x1), width, color, "none");
  if (x1 === x2) return box(slide, x1, Math.min(y1, y2), width, Math.abs(y2 - y1), color, "none");
  const s = slide.shapes.add({
    geometry: "line",
    position: { left: Math.min(x1, x2), top: Math.min(y1, y2), width: Math.abs(x2 - x1), height: Math.abs(y2 - y1) },
    line: { fill: color, width, dash },
  });
  return s;
}
function header(slide, title, page, subtitle = "") {
  slide.background.fill = white;
  box(slide, 0, 682, 1280, 38, blue, "none");
  box(slide, 0, 73, 1280, 3, blue, "none");
  box(slide, 10, 13, 150, 42, white, blue, true);
  text(slide, "byte force", 18, 20, 134, 25, { size: 18, align: "center" });
  text(slide, title, 185, 20, 840, 38, { size: 27, bold: true, font: "Georgia", align: "center", verticalAlign: "middle" });
  if (subtitle) text(slide, subtitle, 215, 52, 780, 16, { size: 11, italic: true, align: "center", color: "#555555" });
  text(slide, "SMART INDIA\nHACKATHON\n2025", 1082, 12, 176, 52, { size: 14, bold: true, color: "#405B66", align: "center", verticalAlign: "middle" });
  text(slide, String(page), 1198, 691, 30, 18, { size: 13, bold: true, color: white, align: "center" });
}
function section(slide, label, x, y, w) {
  text(slide, label, x, y, w, 30, { size: 21, bold: true, color: darkBlue, font: "Georgia" });
  line(slide, x, y + 29, x + Math.min(w, 240), y + 29, darkBlue, 1);
}
function bulletList(slide, items, x, y, w, h, size = 17) {
  const value = items.map(item => `•  ${item}`).join("\n");
  return text(slide, value, x, y, w, h, { size, font: "Georgia" });
}
function labelBox(slide, label, x, y, w, h, fill, color = black) {
  box(slide, x, y, w, h, fill, blue, true);
  text(slide, label, x + 5, y + 5, w - 10, h - 10, { size: 15, bold: true, color, align: "center", verticalAlign: "middle" });
}

// 1. Title page
{
  const s = ppt.slides.add();
  s.background.fill = white;
  text(s, "SMART INDIA HACKATHON 2025", 145, 35, 860, 55, { size: 38, bold: false, color: darkBlue, font: "Georgia", align: "center" });
  text(s, "SMART INDIA\nHACKATHON\n2025", 1080, 24, 170, 72, { size: 16, bold: true, color: "#405B66", align: "center" });
  text(s, "TITLE PAGE", 420, 145, 440, 50, { size: 33, bold: true, font: "Georgia", align: "center" });
  const bullets = [
    "Problem Statement ID - 26075",
    "Problem Statement Title - CAPACITY CONNECT A Digital Capacity Building and Learning Management Portal",
    "Theme - Smart Education",
    "PS Category - Software",
    "Team ID -",
    "Team Name - byte force",
  ];
  bulletList(s, bullets, 48, 235, 820, 380, 23);
  box(s, 840, 175, 300, 330, "#F1F5F8", "#E5EBEF", true);
  text(s, "CC", 885, 225, 210, 100, { size: 78, bold: true, color: blue, align: "center" });
  text(s, "LEARN\nCONNECT\nGROW", 885, 345, 210, 95, { size: 23, bold: true, color: darkBlue, align: "center" });
  s.speakerNotes.textFrame.setText("Reference layout: SIH 2025 title slide supplied by the user. Project metadata supplied by the user.");
}

// 2. Problem and solution
{
  const s = ppt.slides.add();
  header(s, "Capacity Connect: Digital Capacity Building and Learning Management Portal", 2);
  line(s, 568, 83, 568, 246, blue, 1);
  section(s, "Problem", 25, 87, 490);
  text(s, "Capacity-building programmes often keep learning resources, trainee progress, assessment results, and trainer expertise in separate places. Administrators have limited visibility into approvals, course completion, and competency coverage.", 25, 125, 510, 115, { size: 19, font: "Georgia" });
  section(s, "Our Idea", 590, 87, 460);
  text(s, "Capacity Connect brings role-based learning, competency mapping, assessments, certificates, and resource sharing into one portal. It gives trainees, trainers, and administrators a shared operational view.", 590, 125, 635, 115, { size: 19, font: "Georgia" });
  line(s, 0, 248, 1280, 248, blue, 1);
  section(s, "Proposed Solution", 25, 255, 470);
  bulletList(s, [
    "Role-based accounts with administrator approval for new registrations.",
    "Course catalogue with enrollment, progress tracking, feedback, and linked resources.",
    "Timed MCQ assessments that calculate scores and issue certificates after a pass.",
  ], 25, 295, 490, 335, 17);
  section(s, "Innovation / Uniqueness", 850, 255, 380);
  bulletList(s, [
    "One workflow connects learning activity with trainer competencies.",
    "Certificates and assessment outcomes become part of each learner profile.",
    "Administrators can monitor users, approvals, courses, submissions, and announcements from one console.",
  ], 850, 295, 385, 310, 17);
  // Editable solution map
  labelBox(s, "Capacity\nConnect", 535, 390, 205, 76, "#DBEDFB", darkBlue);
  labelBox(s, "Courses &\nResources", 355, 505, 150, 56, paleGold);
  labelBox(s, "Assessments &\nCertificates", 555, 515, 165, 56, paleGreen);
  labelBox(s, "Competency\nMapping", 755, 505, 150, 56, "#F4EAFB");
  line(s, 605, 467, 430, 505, darkBlue, 1.5);
  line(s, 635, 467, 635, 515, darkBlue, 1.5);
  line(s, 670, 467, 830, 505, darkBlue, 1.5);
  s.speakerNotes.textFrame.setText("Solution details based on app.py, models.py, and route modules in the Capacity Connect prototype.");
}

// 3. Technical approach
{
  const s = ppt.slides.add();
  header(s, "TECHNICAL APPROACH", 3);
  line(s, 375, 78, 375, 680, "#D66060", 1, "dash");
  text(s, "Technology Stack", 15, 95, 330, 28, { size: 20, bold: true, font: "Georgia" });
  bulletList(s, [
    "Flask routes and Jinja templates render the web interface.",
    "Tailwind CSS, Lucide icons, Chart.js, and Google Fonts shape the UI.",
    "Flask-SQLAlchemy and SQLAlchemy manage application data.",
    "SQLite stores users, courses, assessments, enrolments, certificates, and more.",
    "Werkzeug hashes passwords and safely names uploaded files.",
    "Local static uploads store learning resources and external certificates.",
  ], 12, 133, 346, 465, 16);
  section(s, "Application Flow", 395, 92, 400);
  labelBox(s, "Sign in / Registration", 460, 145, 195, 42, "#E8F4FC", darkBlue);
  labelBox(s, "Role-based Dashboard", 460, 215, 195, 42, paleGreen, darkBlue);
  labelBox(s, "Courses, Resources & Enrollment", 420, 285, 275, 46, paleGold, darkBlue);
  labelBox(s, "Assessment Submission", 455, 360, 205, 42, "#F4EAFB", darkBlue);
  labelBox(s, "Score, Certificate & Progress Update", 410, 430, 295, 46, "#E8F4FC", darkBlue);
  line(s, 557, 188, 557, 215, darkBlue, 2);
  line(s, 557, 258, 557, 285, darkBlue, 2);
  line(s, 557, 331, 557, 360, darkBlue, 2);
  line(s, 557, 402, 557, 430, darkBlue, 2);
  section(s, "Data and Storage", 760, 92, 395);
  labelBox(s, "Browser\nJinja + Tailwind", 820, 165, 210, 65, "#EAF7F2", darkBlue);
  labelBox(s, "Flask\nBlueprint routes", 820, 270, 210, 65, "#E9F4FC", darkBlue);
  labelBox(s, "SQLAlchemy\nmodels", 820, 375, 210, 65, paleGold, darkBlue);
  labelBox(s, "SQLite DB +\nstatic/uploads", 820, 480, 210, 65, "#F4EAFB", darkBlue);
  line(s, 925, 230, 925, 270, darkBlue, 2);
  line(s, 925, 335, 925, 375, darkBlue, 2);
  line(s, 925, 440, 925, 480, darkBlue, 2);
  box(s, 750, 590, 450, 62, "#AFC8E5", "#8CAFCF");
  text(s, "Functional local web prototype\nCore LMS workflows are implemented", 770, 603, 410, 35, { size: 16, bold: true, color: darkBlue, align: "center" });
  s.speakerNotes.textFrame.setText("Technology statements based on requirements.txt, config.py, app.py, models.py, templates/base.html, and routes/*.py.");
}

// 4. Feasibility and viability
{
  const s = ppt.slides.add();
  header(s, "FEASIBILITY AND VIABILITY", 4);
  line(s, 640, 78, 640, 680, "#D66060", 1, "dash");
  line(s, 0, 424, 1280, 424, "#D66060", 1, "dash");
  section(s, "Feasibility", 15, 88, 400);
  bulletList(s, [
    "The working prototype already covers accounts, approvals, courses, enrolments, assessments, certificates, and resources.",
    "Flask and SQLite support rapid local deployment with low infrastructure requirements.",
    "The data model separates users, learning activity, trainer competencies, and content records.",
    "Server-rendered pages keep the initial implementation straightforward to maintain.",
  ], 15, 126, 590, 270, 17);
  section(s, "Commercial Feasibility", 665, 108, 440);
  bulletList(s, [
    "A shared portal can replace fragmented trackers and manual approval workflows.",
    "Role-based access supports internal academies, training partners, and public-sector capacity programmes.",
    "The modular data model can move from SQLite to a managed database as usage grows.",
    "The platform can add organisation-specific course catalogues and reporting without changing its core user journeys.",
  ], 665, 150, 560, 245, 17);
  section(s, "Challenges", 15, 435, 350);
  bulletList(s, [
    "Demo quick-login and automatic admin access need removal before deployment.",
    "File uploads need extension validation, virus scanning, and managed storage.",
    "SQLite and local files limit concurrent, multi-server operation.",
    "Forms need CSRF protection and stronger audit trails.",
  ], 15, 470, 590, 190, 17);
  section(s, "Strategy", 665, 435, 350);
  bulletList(s, [
    "Deploy a production Flask configuration with environment-managed secrets.",
    "Use PostgreSQL and object storage for a multi-organisation rollout.",
    "Add audit logs, notification workflows, and reporting exports.",
    "Pilot with a focused learner cohort, then refine flows from completion and assessment feedback.",
  ], 665, 470, 560, 190, 17);
  s.speakerNotes.textFrame.setText("Feasibility assessment is an engineering assessment based on the current prototype implementation. It does not assert market-size figures.");
}

// 5. Impact and benefits
{
  const s = ppt.slides.add();
  header(s, "IMPACT AND BENEFITS", 5);
  line(s, 690, 78, 690, 680, "#D66060", 1, "dash");
  line(s, 0, 432, 690, 432, "#D66060", 1, "dash");
  section(s, "Direct Impact on Target Users", 15, 94, 570);
  bulletList(s, [
    "Trainees see a clear path from enrollment to assessment and certification.",
    "Trainers can publish resources, create questionnaires, and review learner performance.",
    "Administrators can approve users, assign roles, monitor activity, and publish announcements.",
    "Programme managers can identify skill coverage through competency mapping.",
  ], 15, 135, 645, 250, 18);
  section(s, "Strategic Impact", 15, 445, 360);
  bulletList(s, [
    "Creates a traceable learning record instead of isolated spreadsheets and files.",
    "Connects trainer expertise with courses and learners' assessed outcomes.",
    "Supports repeatable capacity-building operations across different subject areas.",
  ], 15, 485, 645, 155, 18);
  section(s, "Institutional Benefits", 715, 110, 445);
  bulletList(s, [
    "A central course and resource library reduces duplicated distribution effort.",
    "Certificates provide a verifiable public reference through unique codes.",
    "Course feedback creates a direct channel for improving learning content.",
    "Dashboard metrics consolidate participation, assessment, and completion signals.",
  ], 715, 150, 505, 220, 17);
  // Editable relationship illustration
  text(s, "Capacity-building feedback loop", 805, 405, 350, 25, { size: 18, bold: true, color: darkBlue, align: "center" });
  labelBox(s, "Learn", 760, 470, 105, 52, "#E8F4FC", darkBlue);
  labelBox(s, "Assess", 920, 470, 105, 52, paleGold, darkBlue);
  labelBox(s, "Certify", 1080, 470, 105, 52, paleGreen, darkBlue);
  labelBox(s, "Improve\ncontent", 920, 570, 105, 56, "#F4EAFB", darkBlue);
  line(s, 865, 496, 920, 496, darkBlue, 2);
  line(s, 1025, 496, 1080, 496, darkBlue, 2);
  line(s, 1133, 522, 972, 570, darkBlue, 2);
  line(s, 920, 598, 812, 522, darkBlue, 2);
  s.speakerNotes.textFrame.setText("Impact statements describe intended operational benefits from the implemented Capacity Connect workflows.");
}

// 6. Research and analysis
{
  const s = ppt.slides.add();
  header(s, "Research and Analysis", 6);
  line(s, 640, 78, 640, 680, "#D66060", 1, "dash");
  line(s, 0, 270, 1280, 270, "#D66060", 1, "dash");
  line(s, 0, 470, 1280, 470, "#D66060", 1, "dash");
  section(s, "Gap and Problem Identification", 15, 88, 530);
  bulletList(s, [
    "Map the current learning journey: registration, approval, enrollment, assessment, certification, and profile evidence.",
    "Identify where separate systems create duplicate records or delay programme reporting.",
  ], 15, 126, 575, 120, 16);
  section(s, "Institutional Landscape", 665, 88, 500);
  bulletList(s, [
    "Interview trainees, trainers, and administrators to prioritise dashboard metrics and evidence requirements.",
    "Define data-retention, privacy, and certificate-verification rules for the adopting organisation.",
  ], 665, 126, 555, 120, 16);
  section(s, "Competitive and Workflow Analysis", 15, 285, 560);
  bulletList(s, [
    "Compare current manual processes with a single portal for resources, assessments, certificates, and competency mapping.",
    "Assess integration needs for existing identity, reporting, or content systems before rollout.",
  ], 15, 323, 575, 122, 16);
  section(s, "Prototype Evaluation", 665, 285, 470);
  bulletList(s, [
    "Test the current prototype with representative roles and record task completion, errors, and usability feedback.",
    "Verify that assessment scoring, enrolment completion, certificate generation, and uploaded-resource access work end to end.",
  ], 665, 323, 555, 122, 16);
  section(s, "Technology Benchmarking", 15, 485, 500);
  bulletList(s, [
    "Benchmark local SQLite and file uploads against managed database and object-storage options for scale and resilience.",
    "Assess deployment controls: CSRF, secure sessions, audit logs, backup, and role-permission tests.",
  ], 15, 523, 575, 120, 16);
  section(s, "Pilot and Governance", 665, 485, 440);
  bulletList(s, [
    "Run a limited cohort pilot and measure enrollment, assessment completion, certificate issuance, and feedback use.",
    "Document ownership for content, trainer competency verification, data protection, and support operations.",
  ], 665, 523, 555, 120, 16);
  s.speakerNotes.textFrame.setText("Research plan for the Capacity Connect solution. No external statistics or unsupported results are presented.");
}

await (await PresentationFile.exportPptx(ppt)).save(candidatePath);
const requirements = {
  explicitTotalSlideCount: 6,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
};
const result = await finalizePresentation({
  ...requirements,
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-bullet-geometry", "--validate-heading-fit"],
  fontPolicy: { basis: "design", families: [font, "Georgia", "Arial"] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(buildDir, "capacity-connect-final.validation.json"),
});
console.log(JSON.stringify({ font, finalPath, result }, null, 2));
