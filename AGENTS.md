# KoroFlow workflow repository

For production planning and paid submission, read `skills/koroflow/references/production-standard.md`. Present a concrete plan, exact model tier and parameters, inputs, real-time estimated costs and authorization scope before paid submission unless that exact scope is already explicitly authorized. Use `templates/production-confirmation.md` for the reviewable handoff. The confirmation is an operator workflow, not a claimed programmatic budget lock. Keep local role/account/target settings separate from portable defaults.

For complete video workflows, read `skills/koroflow/SKILL.md`. Preserve the user's chosen production/publishing platforms and local quality rules. Haiyi/Hypit is an existing adapter, documented in `skills/hypit-haiyi/SKILL.md`; the local generic core is `scripts/koroflow.py`. Core records do not invoke platforms. Do not create a false connector or claim a configured descriptor proves live connectivity. Local paths remain in ignored configuration.

For reference recreation batches, follow `skills/koroflow/references/reference-production-runbook.md`: check existing and external outputs, preserve source facts, map source responsibilities to target identities and voices, inspect only the needed assets, bind actual request indices and hashes, then receive, review and hand off real versions. Explicit production instructions can authorize their scope without repeated fixed-word approval. Keep candidate access, requested file handoff, quality acceptance and adoption separate; never falsify quality reviews to pass a delivery gate. Asset counts, time limits and historical prices are project-specific.

Keep video projects separate from the tool and Provider installation. Use `scripts/workflow.mjs init` for new projects. Never replace an existing production with the demo prompt.

For integration development, use the commit pinned in `upstream.json`. Run `node scripts/workflow.mjs verify` after changing Provider behavior or execution/setup helpers. This performs offline mock tests and Source/plan validation, not paid generation. Check skill metadata with the installed skill-creator validator when available.

Never commit `.local`, credentials, node_modules, runtime databases or generated customer media. Keep package distribution source-only using `scripts/bundle.mjs`. Do not publish the repository or submit paid generation simply to validate installation.

Preserve upstream attribution and terms from `NOTICE.md` and `third-party/HYPIT-LICENSE`. Do not describe this integration as an official joint plugin or claim live generation was verified by mock tests.

For delivery records, production counts or publication planning, read `skills/koro-operations/SKILL.md`. Its Python CLI performs offline checks only. Run `python -X utf8 -m unittest discover -s tests -p "test_*.py" -v` after changing operations or packaging; use an available Python 3.11+ interpreter. Keep production-target and publishing-account registries separate. Preserve manual ledger fields by stable IDs and distinguish proposed plans, confirmed schedules and verified platform publications.

The plugin uses root `plugin.json` and a repo catalog at `.agents/plugins/marketplace.json`. Source bundles must retain the explicit allowlist in `scripts/bundle.mjs`; never bundle whole local skill folders containing generated path indexes or runtime caches. Do not add local account records, device addresses, customer files or evidence screenshots to public examples.

The core journal lives in user workspaces under `.koroflow`, never in source distribution. Quality reviews bind actual file hashes; revisions preserve work_id and first delivery date. Use isolated temporary workspaces in tests. `bridge` exports only actual core events to the existing project format; it never refreshes Excel or fabricates successful platform jobs. Existing projects need explicit legacy import, not re-registration as new works. Keep prepared/submitted/unknown/scheduled/published states distinct and preserve unknown outcomes before retries.
