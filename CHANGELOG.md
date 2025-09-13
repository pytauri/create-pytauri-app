# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- `Highlights` for the most attractive new features.
- `BREAKING` for breaking changes.
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.
- `Docs` for documentation changes.
- `YANKED` for deprecated releases.
- `Internal` for internal changes. Only for maintainers.

<!-- Refer to: https://github.com/olivierlacan/keep-a-changelog/blob/main/CHANGELOG.md -->
<!-- Refer to: https://github.com/pytauri/pytauri/blob/main/CHANGELOG.md -->

## [Unreleased]

### Fixed

- [#20](https://github.com/pytauri/create-pytauri-app/pull/20) - fix: fix Linux and macOS build scripts.

    - Pass the `libpython` path correctly on Linux and macOS as `-L` arguments to `RUSTFLAGS`.
    - Temporarily disable `appimage` bundle target

        Currently unable to build `appimage`, see <https://github.com/python-pillow/Pillow/issues/9198>.

    - Change the default `identifier` to `com.username.{{ project_name }}`

        Tauri no longer recommends identifiers ending with `.app`, see <https://github.com/tauri-apps/tauri/issues/12674>.

### Security

- [#19](https://github.com/pytauri/create-pytauri-app/pull/19) - chore(deps-dev): bump vite from 6.3.5 to 6.3.6 in the npm_and_yarn group across 1 directory.

    bump `vite` to `6.3.6` to fix security advisory.

## [0.4.0]

### Added

- [#18](https://github.com/pytauri/create-pytauri-app/pull/18) - feat: bump `pytauri` to `v0.8`.

    - bump `pytauri` monorepo to `v0.8`
    - bump `python-build-standard` to `20250828`

### Changed

- [#16](https://github.com/pytauri/create-pytauri-app/pull/16) - fix(build): bump `setuptools >= 80` for `build-system`.

### Internal

- [#16](https://github.com/pytauri/create-pytauri-app/pull/16) - chore: explicitly require `uv >= 0.8.14` for development.

## [0.3.0]

### Added

- [#14](https://github.com/pytauri/create-pytauri-app/pull/14) - feat: bump `pytauri` to `v0.7`.

## [0.2.0]

### Highlights

- [#10](https://github.com/pytauri/create-pytauri-app/pull/10) - feat: add svelte support.

### Added

- [#7](https://github.com/pytauri/create-pytauri-app/pull/7) - feat: add pytauri home link to template.

### Changed

- [#7](https://github.com/pytauri/create-pytauri-app/pull/7) - feat: update to pytauri `v0.6.0`.
    - Bump all pytauri packages to `0.6`
    - Migrate for pytauri `v0.6` [breaking changes](https://pytauri.github.io/pytauri/0.6/CHANGELOG/)
    - Bump `pyo3` to `0.25`

## [0.1.0]

[unreleased]: https://github.com/pytauri/create-pytauri-app/tree/HEAD
[0.4.0]: https://github.com/pytauri/create-pytauri-app/releases/tag/v0.4.0
[0.3.0]: https://github.com/pytauri/create-pytauri-app/releases/tag/v0.3.0
[0.2.0]: https://github.com/pytauri/create-pytauri-app/releases/tag/v0.2.0
[0.1.0]: https://github.com/pytauri/create-pytauri-app/releases/tag/v0.1.0
