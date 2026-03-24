# Outreach CRM for Mega-OS

A plug-and-play LinkedIn outreach CRM. Drop this folder into any Mega-OS project's `products/` directory to get:

- One-click LinkedIn profile capture (Chrome extension)
- AI-powered personalized message generation (via Claude Code)
- Full pipeline tracking: captured -> generated -> sent -> replied -> interested
- Auto-integration with `business/network/contacts.md`

## Setup

### 1. Configure your outreach identity

Copy the config template and fill it in:

```bash
cp products/outreach-crm/templates/outreach-config-template.json business/network/outreach-config.json
```

Edit `business/network/outreach-config.json` with your name, org, and who you want to reach. Or run `/outreach setup` in Claude Code to do it interactively.

### 2. Start the receiver

```bash
cd products/outreach-crm/receiver
bash start.sh
```

Verify it's running:

```bash
curl http://127.0.0.1:7799/health
```

The receiver runs in the background on port 7799. It saves captured profiles as JSON files. No dependencies beyond Python 3.

### 3. Install the Chrome extension

1. Open `chrome://extensions` in Chrome
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the `products/outreach-crm/extension/` directory
5. Pin the extension to your toolbar

### 4. Create data files

Run `/outreach setup` in Claude Code, or manually:

```bash
cp products/outreach-crm/templates/outreach-queue-template.md business/network/outreach-queue.md
cp products/outreach-crm/templates/outreach-log-template.md business/network/outreach-log.md
mkdir -p business/network/captures/processed
```

### 5. Capture your first profile

1. Navigate to any LinkedIn profile
2. Click the Outreach Capture extension button
3. Wait for "Saved!" confirmation
4. In Claude Code, run `/outreach process`

## Usage

| Command | What it does |
|---------|-------------|
| `/outreach` | Dashboard: pending captures, pipeline summary, follow-ups due |
| `/outreach setup` | First-time setup (directories, config, verification) |
| `/outreach process` | Process pending captures (generate messages) |
| `/outreach send <name>` | Mark message as sent, update contacts.md |
| `/outreach reply <name>` | Log a response with sentiment |
| `/outreach status` | Analytics: reply rates, best approach, pipeline stats |
| `/outreach import` | Bulk import from CSV |
| `/outreach remind` | Draft follow-up messages for overdue contacts |
| `/outreach delete <name>` | Remove contact from pipeline |

## Stopping the receiver

```bash
cd products/outreach-crm/receiver
bash stop.sh
```

## Troubleshooting

**Extension shows error when clicking capture:**
- Make sure the receiver is running (`bash start.sh`)
- Check `receiver/receiver.log` for errors

**Extension button doesn't appear on LinkedIn:**
- Verify the extension is loaded in `chrome://extensions`
- Refresh the LinkedIn page (content script may not have injected on pre-existing tabs)

**Receiver won't start:**
- Check if port 7799 is already in use: `lsof -i :7799`
- Set a different port: `export OUTREACH_PORT=7800` before `start.sh`

## How it integrates with Mega-OS

- Messages follow the writing style guide (`core/standards/writing-style.md`)
- Sent contacts are added to `business/network/contacts.md` using the Contact Follow-Up Protocol
- Follow-up cadence uses platform defaults from `core/templates/network-contacts-template.md`
- Business context comes from `business/network/outreach-config.json` + `business/sales/icp.md` (if exists)
