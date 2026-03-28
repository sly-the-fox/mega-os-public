# Deployment Checklist

## Known Deploy Targets

Add your deploy targets here. Examples:

| Target | Script | Platform | Command |
|--------|--------|----------|---------|
| Public repo sync | `engineering/scripts/sync-to-public.sh` | GitHub | copies framework files to public repo |
| *(your site)* | *(deploy script path)* | *(Cloudflare / Vercel / Netlify)* | *(deploy command)* |
| *(your package)* | manual | *(PyPI / npm)* | *(build + publish command)* |

## Pre-Deploy

- [ ] Tests pass (if test suite exists)
- [ ] Version bumped in pyproject.toml / package.json (if version change)
- [ ] No uncommitted changes in working tree
- [ ] Secrets/env vars confirmed set in target environment
- [ ] CHANGELOG or commit message documents what changed

## Deploy

- [ ] Run the deploy command / script
- [ ] Watch for errors in output
- [ ] Note deploy timestamp

## Post-Deploy

- [ ] Verify live endpoint responds (curl or browser check)
- [ ] Spot-check key functionality
- [ ] Update `business/marketing/adoption-metrics.md` if relevant
- [ ] If package registry: verify install pulls new version
- [ ] If site: check DNS resolution and HTTPS

## Rollback

- **Static hosting (Cloudflare Pages, Vercel, Netlify):** Revert via dashboard (previous deployment)
- **Package registry (PyPI, npm):** Cannot unpublish — push a patch version with the fix
- **Git-based deploy:** `git revert` + push
- **CMS / managed hosting:** Undo in the platform editor
