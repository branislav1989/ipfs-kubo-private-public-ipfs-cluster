# 🔐 GitHub Personal Access Token - Complete Guide

## Problem You're Facing
Git keeps asking for password but tokens don't work with the interactive prompt.

## Solution
Use a Personal Access Token (PAT) with the helper script we created.

---

## Step 1: Create Your Personal Access Token

1. **Go to GitHub Settings:**
   - Visit: https://github.com/settings/tokens

2. **Click "Generate new token (classic)"**
   - NOT the "Generate new token (fine-grained)"
   - Use the CLASSIC version

3. **Fill in the form:**
   - Token name: `RSS Curation Deploy`
   - Expiration: 90 days (or longer if you prefer)
   
4. **Select Scopes (permissions):**
   - ✅ `repo` - Full control of private repositories
   - ✅ `workflow` - Update GitHub Actions and workflows
   - (Leave others unchecked)

5. **Click "Generate token"**

6. **COPY the token immediately!**
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You won't see it again after you leave the page!

---

## Step 2: Use the Token to Push

Run our helper script:

```bash
bash rss_curation/PUSH_WITH_TOKEN.sh
```

When it asks for your token:
- Paste the token you just copied
- Press Enter
- It will push automatically!

---

## Step 3: Verify Success

After successful push:
- Visit: https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster
- Check that `rss_curation/` folder appears
- Check `.github/workflows/` folder

Done! 🎉

---

## Troubleshooting

### Token keeps being rejected
- Make sure you copied the ENTIRE token
- Make sure it starts with `ghp_`
- Generate a new token if unsure

### "repo" scope not available
- You must use "classic" token, not "fine-grained"
- Go back to https://github.com/settings/tokens
- Look for "Generate new token (classic)"

### Token expired
- Tokens expire after the set period
- Generate a new one
- Use the new token to push

---

## Important Notes

✅ **DO:**
- Keep your token SECRET (never share it)
- Copy the entire token
- Use the helper script

❌ **DON'T:**
- Share your token with anyone
- Commit token to repository
- Use your GitHub password instead of token

---

## Quick Command Reference

If you want to push manually without the script:

```bash
git push https://branislav1989:YOUR_TOKEN@github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster.git master
```

Replace `YOUR_TOKEN` with your actual token!

---

## Need Help?

- Token help: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- Push help: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository

