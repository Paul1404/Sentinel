# CHANGELOG

<!-- version list -->

## v0.3.16 (2025-08-30)

### Bug Fixes

- Remove : from pipeline job
  ([`c5b3e73`](https://github.com/Paul1404/Sentinel/commit/c5b3e735290096cc6b4d18ee0516bd6f51be28c1))

### Chores

- Ci(copr): add debug output for binary, spec, SRPM, and copr-cli config
  ([`4638364`](https://github.com/Paul1404/Sentinel/commit/46383646be4c827c8c4db61f76e32c87e4e89c8c))

- Ci(copr): add separate COPR packaging workflow using latest GitHub release binary
  ([`cf3b487`](https://github.com/Paul1404/Sentinel/commit/cf3b48746b1829044892f8168f1c5c8d7312563b))


## v0.3.15 (2025-08-30)

### Bug Fixes

- Ci(copr): fix spec changelog date and ensure valid copr-cli config
  ([`d2bc49a`](https://github.com/Paul1404/Sentinel/commit/d2bc49a94e71a6d06429bb3045ce3229ac2e49da))


## v0.3.14 (2025-08-30)


## v0.3.13 (2025-08-30)

### Bug Fixes

- Trigger CI
  ([`9331229`](https://github.com/Paul1404/Sentinel/commit/9331229e31be7a671ca5b72c0d860b0a554fc3c1))

### Chores

- Ci(workflow): rewrite release pipeline with Nuitka build, smoke test, GitHub release, and COPR RPM
  publish
  ([`2870eb4`](https://github.com/Paul1404/Sentinel/commit/2870eb4fb8a2f7e2a3e0ab7cb2b619b062343032))


## v0.3.12 (2025-08-30)

### Bug Fixes

- Ci(workflow): use CentOS container for COPR RPM build and upload
  ([`2da96b8`](https://github.com/Paul1404/Sentinel/commit/2da96b8d5116ac4fe0f4432be626d4d5669683fc))


## v0.3.11 (2025-08-30)

### Bug Fixes

- Trigger Release Workflow as Test
  ([`7345dfd`](https://github.com/Paul1404/Sentinel/commit/7345dfd25881f601f3c9377aa8d2a681d2cc7f04))

### Chores

- Ci(workflow): finalize release pipeline with GitHub binary + COPR RPM publish
  ([`aa7d443`](https://github.com/Paul1404/Sentinel/commit/aa7d443aa28c2bf45aacee4c49302fcce34c9508))

- Ci(workflow): refactor release pipeline with ccache, containerized build, and smoke test
  ([`1e2de30`](https://github.com/Paul1404/Sentinel/commit/1e2de302adc8ce8f1df401ba7a630c8a12240937))


## v0.3.10 (2025-08-30)


## v0.3.9 (2025-08-30)

### Bug Fixes

- Ci(workflow): refactor release pipeline to build only in manylinux and add smoke test
  ([`46b3e14`](https://github.com/Paul1404/Sentinel/commit/46b3e149a921bee6d210a07d8ea7b0d2782fabcd))


## v0.3.8 (2025-08-30)

### Bug Fixes

- Ci(workflow): install project dependencies before Nuitka build
  ([`d3d5b28`](https://github.com/Paul1404/Sentinel/commit/d3d5b286c90099775a7a29c3356cdcac7014e71d))


## v0.3.7 (2025-08-30)

### Bug Fixes

- Ci(workflow): fix Nuitka build to include dependencies (typer, rich)
  ([`f70bb66`](https://github.com/Paul1404/Sentinel/commit/f70bb66a673cecf72fb5071b77723be72ed956c5))


## v0.3.6 (2025-08-30)

### Bug Fixes

- Ci(workflow): fix Nuitka build by unpacking static libpython in manylinux container
  ([`b5c5a80`](https://github.com/Paul1404/Sentinel/commit/b5c5a80d241864e905519bae82b6ff2a66eb2732))


## v0.3.5 (2025-08-30)

### Bug Fixes

- Set --static-libpython=no
  ([`92163a8`](https://github.com/Paul1404/Sentinel/commit/92163a824da1bd0f2bf86d6b4ff20b12631a3323))


## v0.3.4 (2025-08-30)

### Bug Fixes

- Drop --static-libpython
  ([`d888e93`](https://github.com/Paul1404/Sentinel/commit/d888e93aea1a71298b73ed015edf31d3b408085f))


## v0.3.3 (2025-08-30)

### Bug Fixes

- Test New Release Workflow
  ([`7f98553`](https://github.com/Paul1404/Sentinel/commit/7f9855378b1969162d378cd36d72a0320e097873))


## v0.3.2 (2025-08-30)

### Bug Fixes

- Remove Binary Strip from ci
  ([`ff2ccf2`](https://github.com/Paul1404/Sentinel/commit/ff2ccf2b6a0eec43e460c6baf0402e9739b5f7c9))


## v0.3.1 (2025-08-30)

### Bug Fixes

- Make nuitka floating
  ([`0d79d3a`](https://github.com/Paul1404/Sentinel/commit/0d79d3a5c269fb9e6d429bd62e85988145dfa0b1))


## v0.3.0 (2025-08-30)

### Features

- Add README for release pipeline with mermaid diagram
  ([`70e38a9`](https://github.com/Paul1404/Sentinel/commit/70e38a9e248c540da5584020e45f28409153626a))


## v0.2.1 (2025-08-30)

### Bug Fixes

- Forgot to install pip
  ([`9e8ddcf`](https://github.com/Paul1404/Sentinel/commit/9e8ddcf9416e65926c8c521c9cb0878537e7a294))


## v0.2.0 (2025-08-30)

### Bug Fixes

- Remove debug step from semantic-release and streamline the publish command
  ([`ca95b94`](https://github.com/Paul1404/Sentinel/commit/ca95b948a337979ff0a5ca651ed5fd4bc3452efd))

### Chores

- Run semantic-release before Nuitka build and enable ccache + Nuitka cache
  ([`0582e96`](https://github.com/Paul1404/Sentinel/commit/0582e962cfef60b0cf5e7359119eb0f94d19141e))

- Switch to python-semantic-release gh action
  ([`d468eef`](https://github.com/Paul1404/Sentinel/commit/d468eefe04fe98066e42bfff8a85f93e9baa1645))

### Features

- Add debug step for semantic-release to improve output visibility
  ([`d7ca74d`](https://github.com/Paul1404/Sentinel/commit/d7ca74d6ce97117042b8b4fec83068d229218d4c))


## v0.1.0 (2025-08-29)

- Initial Release
