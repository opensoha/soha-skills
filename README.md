# soha-skills

This repository owns OpenSoha's official skills, MCP presets, and agent profiles.

Soha's open-source core should consume these assets through published artifacts,
manifests, configured directories, or other explicit integration points. Do not
copy business logic between this repository and `github.com/opensoha/soha`.

## Layout

```text
soha-skills/
  skills/          # Official Soha skills
  mcp-presets/     # MCP preset manifests and examples
  agent-profiles/  # Agent profile manifests and examples
```

The initial `skills/` content was copied from `soha/skills` as a low-risk split.

## Boundary

- This repository owns skill and preset source assets.
- `soha` remains the open-source core and runtime integration point.
- Cloud-only behavior belongs outside this repository unless exposed as a
  generic, open extension asset.
- Generated output should be published as versioned artifacts rather than
  committed here by default.

## License

This repository is licensed under the Apache License 2.0. See
[LICENSE](./LICENSE) for the full license text.
