# Public IBM QRadar SOAR Apps

This repository contains sanitized, public IBM QRadar SOAR applications.
Working development is performed outside this Git repository in the sibling
`work/<app_name>` directory. Only reviewed and cleaned application sources are
copied here.

Applications live under:

```text
apps/<app_name>
```

Container images are published to GitHub Container Registry using this format:

```text
ghcr.io/bellka-p/<app_name>:<version>
```

Installable IBM SOAR ZIP packages are not stored in this repository. They are
built locally after the corresponding container image has been published.

## Versioning

For every release, the same version must be used in:

- Python package metadata in `setup.py`;
- IBM SOAR package metadata;
- the container image tag;
- the Git tag.

Example for version `1.0.1`:

```text
Python/SOAR: 1.0.1
Image:       ghcr.io/bellka-p/fn_test_app:1.0.1
Git tag:     fn_test_app-v1.0.1
```

Pushing a tag matching `<app_name>-v<version>` runs the image workflow for that
one application. The workflow does not build all applications on ordinary
pushes and does not create `latest` automatically.

## Publication procedure

Development starts in `../work/<app_name>`. Before copying an app here:

1. Run its complete unit-test suite.
2. Scan the working tree for secrets, including these terms and signatures:

   ```text
   password
   passwd
   secret
   token
   api_key
   apikey
   authorization
   bearer
   private key
   BEGIN RSA
   BEGIN PRIVATE
   client_secret
   access_token
   ```

   A basic review command (not a replacement for a dedicated secret scanner):

   ```shell
   rg -n -i '(password|passwd|secret|token|api[_-]?key|apikey|authorization|bearer|private[ _-]?key|BEGIN RSA|BEGIN PRIVATE|client_secret|access_token)' ../work/<app_name>
   ```

3. Inspect `app.config`, `.env*`, credentials, certificates, private keys,
   hardcoded API keys, internal credentials, and Docker authentication data.
4. Do not copy virtual environments, `build`, `dist`, logs, test output,
   `.env*`, real `app.config` files, secrets, or local Docker configuration.
5. If configuration documentation is required, create `app.config.example`
   containing safe placeholder values only.
6. Fully synchronize only sanitized and necessary files from
   `../work/<app_name>` to `apps/<app_name>`.
7. Repeat the secret scan against `apps/<app_name>` after synchronization.

   ```shell
   rg -n -i '(password|passwd|secret|token|api[_-]?key|apikey|authorization|bearer|private[ _-]?key|BEGIN RSA|BEGIN PRIVATE|client_secret|access_token)' apps/<app_name>
   ```
8. Before requesting a commit, show and review:
   - the complete application file list;
   - `git status`;
   - `git diff`;
   - test results;
   - secret-scan results.

Do not commit, tag, or push automatically. Those actions require an explicit
user command after review.

## Release workflow

After review and an explicitly authorized commit, create a tag such as:

```shell
git tag fn_test_app-v1.0.1
git push origin fn_test_app-v1.0.1
```

The tag triggers `.github/workflows/build-images.yml`, which validates the app
name and version, builds `apps/fn_test_app/Dockerfile`, and publishes:

```text
ghcr.io/bellka-p/fn_test_app:1.0.1
```

The workflow uses `GITHUB_TOKEN`; no registry password is stored in the
repository.
