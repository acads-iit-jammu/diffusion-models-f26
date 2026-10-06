// A nested render rewrites watched HTML/resources. Do not run it on every
// incremental preview rebuild, or those writes can trigger another rebuild.
// See https://quarto.org/docs/projects/scripts.html#pre-and-post-render
const notebookDir = "materials/probability-flow/notebooks";
let missingOutput = false;
for (const entry of Deno.readDirSync(notebookDir)) {
  if (!entry.isFile || !entry.name.endsWith(".ipynb")) continue;
  const html = `${notebookDir}/${entry.name.replace(/\.ipynb$/, ".html")}`;
  try {
    if (!Deno.statSync(html).isFile) missingOutput = true;
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) missingOutput = true;
    else throw error;
  }
}

// Full renders refresh every notebook. A clean checkout also needs its first
// HTML build; later preview events reuse it without touching watched files.
if (Deno.env.get("QUARTO_PROJECT_RENDER_ALL") !== "1" && !missingOutput) {
  Deno.exit(0);
}

const result = await new Deno.Command("quarto", {
  args: ["render", notebookDir],
  stdin: "inherit",
  stdout: "inherit",
  stderr: "inherit",
}).spawn().status;
Deno.exit(result.code);
