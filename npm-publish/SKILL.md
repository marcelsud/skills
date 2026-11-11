---
name: npm-publish
description: Publish a package to the npm registry from a shared or headless machine, including the first publish of a new package and the order of updates in dependent repositories. Use when publishing, preparing a first publish, or coordinating a library release with consumer repositories.
---

# Publish an npm package

Interactive npm website login is a poor fit for a shared or headless
machine: the session typically expires in about five minutes and then
drops. Use a granular access token instead, and keep the token out of
files and logs.

## Create a token that can publish a new package

For the first publish of a package that does not yet exist on the
registry, the token needs read and write access to all packages. A
granular token restricted to selected packages cannot address a package
that does not exist yet; the registry responds with 404 on the PUT that
would create it.

After the package exists, a later rotation may narrow the token to that
package. Do not start from a selected-package token for a brand-new
name.

## Authenticate without writing the token

Export the token in the environment, for example as `NPM_PUBLISH_TOKEN`.
Never paste the literal token into a file, a command line history, a
skill, or a log.

In the user npmrc (`~/.npmrc`), point the npm registry at the environment
variable:

```
//registry.npmjs.org/:_authToken=${NPM_PUBLISH_TOKEN}
```

The `${NPM_PUBLISH_TOKEN}` text is the variable reference, not the
secret. Confirm the file contains the reference and not a token value
before proceeding.

## Publish

Confirm the authenticated identity with `npm whoami`. Then publish with
public access when that is the intended visibility:

```
npm publish --access public
```

If `whoami` fails, stop and repair authentication; do not retry publish
until the identity is confirmed.

After a first publish, the registry may show a `0.0.0-stage` stub for
the package for a few minutes. This is a temporary registry artifact,
not evidence that the published version is wrong. Wait and re-check
before treating it as a failed or rolled-back release.

## Coordinate dependent repositories

When other repositories consume the package, use this order:

1. Merge the library change.
2. Publish the library package.
3. Update the consumer repository's lockfile to the published version.
4. Merge the consumer change.

Do not merge a consumer that depends on a version that has not been
published. Do not update the consumer lockfile from an unpublished
local build when the delivery path is the public registry.

## Protect the token

Unset the environment variable when the work is finished. Do not commit
`.npmrc` files that contain a literal token. If a token may have been
exposed, revoke it and issue a replacement; do not continue to use it.
