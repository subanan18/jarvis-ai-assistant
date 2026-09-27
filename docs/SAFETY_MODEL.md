# JARVIS tool-safety model

JARVIS is designed so conversational output does not automatically become unrestricted operating-system actions.

## Principles

### Explicit capabilities

Desktop actions should be exposed as small, named tools instead of a general-purpose shell executor.

### Allow-listed applications

Application launching should only accept known safe application identifiers that map to approved local executables.

### Restricted generated files

Generated Python files are written only inside `generated_projects/`. User-supplied paths should be normalised and rejected when they escape that workspace.

### Secrets stay local

LiveKit and model credentials belong in `.env.local`, which must remain excluded from Git.

### Human-visible effects

Tools that open programs, create files or navigate websites should produce an understandable confirmation so the user knows what happened.

## Threats to avoid

- Arbitrary shell execution from model text
- Writing outside the approved workspace
- Accidental credential commits
- Unbounded subprocess creation
- Treating web content as trusted instructions

## Future hardening

- Per-tool permission prompts
- Structured audit logging
- Rate limits for repeated desktop actions
- Safer URL/domain handling
- Signed/validated configuration
- Tests for path traversal and allow-list bypass attempts

This document describes the intended security boundary for the project and should evolve with new tools.
