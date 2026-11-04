# Optional orchestration

[hermes-immutable-techniques](https://github.com/smoermeow/hermes-immutable-techniques) is the existing routing/protection architecture, demonstrated with the Creative Orchestrator. Its orchestrator and load guides point to protected methods without rewriting them.

The orchestrator stays in that repository. This collection does not contain a second maintained copy.

To use that architecture with this library, follow its own setup documentation and point its project/load-guide paths at the skill folders you actually keep locally. The orchestrator repository supplies template technique folders; the actual published methods are in this skills library. Refer only to installed skills whose complete required files are available.

Each skill here can also be read directly with a compatible agent. Its README explains inputs, required files and execution dependencies. Adopting an orchestrator is optional.

[Back to the skills library](../README.md)


## Fast initial setup — optional, only for a new installation

Start at [hermes-immutable-techniques](https://github.com/smoermeow/hermes-immutable-techniques), then read its [architecture](https://github.com/smoermeow/hermes-immutable-techniques/blob/main/ARCHITECTURE.md), [canonical in-skill README](https://github.com/smoermeow/hermes-immutable-techniques/blob/main/profiles/creative/skills/creative/creative-orchestrator/README.md), and [route-to-folder contract](https://github.com/smoermeow/hermes-immutable-techniques/blob/main/projects/orchestra-skill-library/README.md). Its tree supplies an orchestrator/load-guide pattern and downstream templates, not the complete methods in this library.

1. Download or clone that repository into a separate staging location. For a **new** setup, copy its complete `profiles/creative/skills/creative/creative-orchestrator/` folder into the chosen Hermes profile's `skills/creative/` location. The repository's `/hermes` is an example mount point, not a universal path. Do not copy an entire profile over an existing one.
2. Keep its `projects/orchestra-skill-library/` template tree at your chosen library location, or point the router at a separately kept technique library. Bring in complete skill folders from this collection without rewriting the methods or flattening their supporting paths.
3. Follow the repository's route-to-folder contract. Set each selected route's `Source project:` and its router-local reference's `Read first:` to the **actual** downstream location. Route names and template folder names need not match this collection's published skill names; never equate similarly named or different-version methods automatically. Register only the targets whose complete files are present.
4. Verify a request selects the intended route, opens its load guide, and reads its complete required method/context. This is a read-only routing check, not permission to generate, upload, or process media. The separate repository also documents an optional profile-local memory preference for broad requests; apply it only in the profile you deliberately choose.

### Already have protection or orchestration?

**Preserve the installed architecture.** Do not reinstall a profile, replace a router, prune unrelated routes, migrate libraries or optimize protected techniques to add one skill. Use that skill README's short registration prompt: inspect the existing layout and make only the approved route/load-guide pointer change. A collision or incompatible contract needs a decision, not a silent replacement. The orchestrator and references route; the downstream skill retains the full method. No local orchestrator changes are performed by reading this guide.
