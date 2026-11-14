jellyfin.bunhub.dev is a live public address that is serving jserver's jellyfin, but implementation is a little raw.

Let's get a proper project set up (vikunja project for corresponding project folder ~/projects/tv-bunhub (which should be connected to the existing (new and empty) repo at github.com/bunhub-dev/tv-bunhub.git.

First steps for what this project is doing: audit the existing jellyfin.bunhub.dev implementation (security flaws, risks the server is/could be publicly exposed to, bad practices, use of best practices vs. anti-patterns).  

Then port everything over to my desired actual production endpoint: tv.bunhub.dev.  This will require cloudflare/DNS work, but existing DNS records should be reviewed as part of the initial audit and pruned to only actually serve (1) jellyfin, (2) bunhub.dev splashpage, and (3) pjs.bunhub.dev which should be ported over from vikunja.bunhub.dev (additionally, auth.bunhub.dev can probably be discarded unless there's a real need for an auth redirect gateway--note: authentik was considered for user/directory integration with jellyfin, jellyseerr, and vikunja; but was removed due to inability to get things working correctly/smoothly/at all)

You're the PM that takes my prompts and turns them into a proper production environment for our new bunhub.dev universe.
