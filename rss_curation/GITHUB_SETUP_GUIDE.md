# GitHub Authentication Setup

The RSS curation files are ready to push to GitHub, but you need to authenticate first.

## Files Ready to Push

- `curated_links.json` - Curated links in JSON format
- `curated_links.md` - Curated links in Markdown format
- `curated_links.html` - Curated links in HTML format
- `daily_update.sh` - Daily update automation script
- `setup_cron.sh` - Cron job setup script
- `README.md` - Documentation

## Authentication Options

### Option 1: SSH Key (Recommended)
1. Generate SSH key if you don't have one:
   ```bash
   ssh-keygen -t ed25519 -C "branislav1989@gmail.com"
   ```

2. Add the public key to GitHub:
   - Go to https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your public key

3. Test connection:
   ```bash
   ssh -T git@github.com
   ```

4. Push to GitHub:
   ```bash
   git push github master
   ```

### Option 2: GitHub Personal Access Token (HTTPS)
1. Create token at https://github.com/settings/tokens
2. Set up credential helper:
   ```bash
   git config --global credential.helper store
   ```
3. Push (it will prompt for token as password):
   ```bash
   git remote set-url github https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster.git
   git push github master
   ```

## Current Status
All files are committed locally and ready to push. Commit: 5c15b31

## Next Steps
1. Choose authentication method
2. Authenticate with GitHub
3. Run: `git push github master`
4. Verify files appear at: https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster
