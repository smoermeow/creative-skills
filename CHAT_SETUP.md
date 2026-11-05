# Chat setup for the text-method skills

Ready-to-paste Project instruction files for Seedance V4, Seedance Narrative, Midjourney Prompts V2 and Storyboard are in [chatgpt-projects/](chatgpt-projects/README.md). Use them with the original context files listed below.

Use **one skill per ChatGPT Project** as the default. A custom GPT, where its editor remains available, or a Gemini Gem can use the same original files and a short routing instruction. This is a way to supply a method to chat, not an agent-plugin installer or a replacement for the complete skill.

## 1. Choose a skill and get its originals

Download this repository with GitHub's **Code → Download ZIP**, or clone it, then open the relevant skill README. Keep the complete downloaded folder intact locally. Upload the actual original method/context files listed below, not this guide, a paraphrase, a stored ZIP, or the README alone. No duplicate method packages are maintained here.

| Skill and copy-ready routing block | Original method/context to upload |
| --- | --- |
| [Midjourney Prompts V2](image/midjourney-prompts-v2/README.md#copy-ready-routing-instructions) | [SKILL.md](image/midjourney-prompts-v2/SKILL.md), [templates/prompt-template.txt](image/midjourney-prompts-v2/templates/prompt-template.txt) |
| [Anime Character Design Lab](image/anime-character-design-lab/README.md#copy-ready-routing-instructions) | [SKILL.md](image/anime-character-design-lab/SKILL.md), [ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md](image/anime-character-design-lab/ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md). Also upload [modern-anime-styles.md](image/anime-character-design-lab/modern-anime-styles.md) if using its supplementary production-style working material. |
| [Seedance Prompter V4](video/seedance/seedance-prompter-v4/README.md#copy-ready-routing-instructions) | [SKILL.md](video/seedance/seedance-prompter-v4/SKILL.md), [instructions.md](video/seedance/seedance-prompter-v4/instructions.md), [seedance-prompter-v4-master-knowledge.md](video/seedance/seedance-prompter-v4/seedance-prompter-v4-master-knowledge.md), plus [references/platform-character-limits.md](video/seedance/seedance-prompter-v4/references/platform-character-limits.md) for named-platform limits. Upload the latter too so it is available when needed. |
| [Seedance Narrative Prompter](video/seedance/seedance-narrative-prompter-v1/README.md#copy-ready-routing-instructions) | [SKILL.md](video/seedance/seedance-narrative-prompter-v1/SKILL.md), [references/knowledge.md](video/seedance/seedance-narrative-prompter-v1/references/knowledge.md) |
| [Storyboard](scripting/storyboard/README.md#copy-ready-routing-instructions) | [SKILL.md](scripting/storyboard/SKILL.md), plus your own idea or blueprint as task input. Full completion also needs Python and file tools; see below. |

Use one skill per Project, custom GPT or Gem to avoid multiple unrelated files named `SKILL.md` and accidental method blending. Upload interfaces may flatten paths: for example, `references/knowledge.md` can appear as `knowledge.md`. Keep the original-path-to-uploaded-name mapping unambiguous. If an interface rejects an original file type, use a supported full-text source without omitting any content, or switch to a file-capable agent; do not silently replace the original with a summary.

## 2. ChatGPT Projects — primary setup

1. Create a **New project** in ChatGPT and name it for the chosen skill.
2. Add the original files above as project files/sources. Check that every required file is present and readable; a GitHub link in a message is not the file upload.
3. Open the project's **••• → Project settings** and paste that skill README's **Copy-ready routing instructions** into **Project instructions**. Keep this block short: it tells ChatGPT which uploaded method to follow; the uploads retain the complete original knowledge.
4. Start a chat **inside that Project** and use the skill README's invocation example with your own brief. Supply duration, constraints, reference roles and exact baseline wording where relevant. Attach actual reference images if the selected model can inspect them.
5. Ask it to identify the required files before drafting. Test one small text-only request and compare the result with the method's actual output contract. If it cannot access the complete required context, stop and fix the missing input rather than letting it improvise.

OpenAI documents projects as keeping chats, uploaded files and project instructions together; project instructions apply in that project. Availability, upload formats, tools and limits depend on the account/workspace. See the official [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) guide; do not rely on a fixed quota in this README.

## 3. Custom GPT — secondary, only where available

If you have an editable custom GPT or an account/workspace that still exposes the editor, use one GPT for the selected method. Put the short routing block in **Instructions**, upload the listed original files under **Knowledge**, and test the result in **Preview** before saving. Keep the instructions explicit about following the uploaded method; do not use an automatic rewrite to replace its knowledge or behavior.

OpenAI's current [Creating and editing GPTs](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts) guide distinguishes Instructions from uploaded Knowledge and includes retirement/migration notices and account/workspace restrictions. Check those notices first: this guide does **not** assume that creating a new GPT is available to everyone. Use a Project when the editor is unavailable. Any enabled Python/file capability must actually be tested before claiming a validated or saved result.

## 4. Gemini Gem — equivalent setup

In the Gemini web app, open **Explore Gems → New Gem**, name the Gem, and paste the selected skill's short routing block into its instructions. Under **Knowledge → Add files**, upload the same original files from your device. Preview the Gem with a small text request, check that it uses the complete method, then **Save**; previewing alone does not save it. Do not ask the instruction-rewrite feature to optimize the protected method.

Google documents those steps and knowledge uploads in [Tips for creating custom Gems](https://support.google.com/gemini/answer/15235603?hl=en). Use the current interface and supported file types available to your account; this guide does not promise a particular quota or automatic GitHub integration.

## 5. Check what the chat can actually do

- **Text prompting/design:** the originals supply the method, not an image/video render. Image-reference work additionally requires real image understanding. Required exact character counts need a counting tool; an estimate is not verified evidence.
- **Storyboard:** chat can help draft, but the complete method requires available Python to run `json.load()`, required-field checks, and a real `.json` file written with file tools. If those tools are absent, request an explicitly labelled draft only, or move to a file-capable agent for completion. Do not call a chat-only draft validated, saved or production-complete. A downloadable sandbox file is not automatically saved next to a blueprint on your computer; establish the actual destination and transfer it deliberately if needed.
- **Execution wrappers/media preparation:** uploading Codex Image, Krea Image Generation, Dreamina or continuation-frame instructions does not install a CLI, plugin, Python environment, account connection or credentials. A text-only chat cannot execute those wrappers. In particular, the current Codex Image adapter remains Hermes-plugin dependent even when another agent drives it. Follow each wrapper's runtime and authorization requirements in its own README; no test render, upload or media-processing job is authorized by setup.

## 6. Keep uploaded copies current

**GitHub links alone are not uploaded context, and these uploads are not live synchronization.** When source files change, download their new originals, remove/replace outdated uploaded copies through the platform's controls, check the filenames and repeat the small method/output test. Refresh the full required set when needed; do not mix different source versions or assume an old chat has reloaded them. This repository provides no auto-sync service or separate per-skill ZIPs.

Official platform guidance was checked on **November 4, 2026**. Interfaces and account availability can change; follow the linked official guides. The short routing instructions are loading directions, never a substitute for the original files.
