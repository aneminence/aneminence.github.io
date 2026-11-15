# VI 2.0 website update

- Source of brand assets: sibling aneminence-brand/assets/logos/svg and design-tokens/source.json. Six SVG exports copied unchanged; original path geometry retained.
- Website colors preserve V1.2 core palette; Craft material gray updated to #737B83. Keep readable small-text neutral separate.
- Inter and Noto Sans SC WOFF2 subsets derive from the supplied OFL fonts. Exact source hashes and byte sizes are in assets/fonts/sources.json; licenses retained.
- New web portfolio compositions use the original V5 components, stationery/hardware concepts and the VI jacket technical flat. Physical applications remain clearly marked as concepts or proof-required design work.
- CMTS card uses a capture of the live introduction site at https://aneminence.github.io/cmts-website/zh/ and links directly to it. The introduction site is live and evolving; hardware imagery remains explicitly labeled as concept imagery, not a released product.
- Existing monochrome mountain artwork remains from the original user-supplied site package. Old assets are retained for cached legacy pages; the current UI uses the new assets.
- Build output is isolated, checks internal anchors, validates public release version and assets after deployment. No credentials, local QA images or VI working documents are published.
