## readme.md
---

The pack command in CPTD CLI enables seamless export and import of CLI commands as ZIP archives. Ideal for backups, sharing tools, or migrating setups across machines.


The pack command is a core utility of CPTD CLI designed to manage the export and import of command modules in .zip format. It simplifies sharing commands between users, creating backups, and migrating CLI configurations across systems. Users can export all installed commands to a directory or import them back with options like --replace and --skip-existing. The tool enforces structural validation and excludes unnecessary files to ensure security. Whether you're managing multiple environments or distributing tools to a team, pack provides a structured and safe way to handle command portability in CPTD.

---

## 📦 New Command: `pack`

**Purpose:**
Exports installed commands into individual `.zip` archives or imports them from a directory. Supports batch transfer of CLI commands between machines and users.

---

## ✅ Arguments

| Argument          | Purpose                                                               |
| ----------------- | --------------------------------------------------------------------- |
| `--export`        | Export all installed commands as `.zip` files to the specified folder |
| `--import`        | Import `.zip` files from the specified folder                         |
| `--output`        | (with `--export`) path to the folder where ZIPs will be saved         |
| `--from`          | (with `--import`) path to the folder to read ZIPs from                |
| `--replace`       | Remove all current commands before importing                          |
| `--skip-existing` | Skip commands that are already installed                              |

---

## 📦 `pack` Command — Export and Import CLI Commands in CPTD

The `pack` command allows you to export installed commands into `.zip` archives and import them back. It is ideal for backup, command sharing, creating themed bundles, and migrating CLI setups.

---

### 🧰 Use Cases

* Export each installed command into an individual `.zip` file
* Import `.zip` files from a specified directory
* Supports flags: `--replace`, `--skip-existing`

---

### ✅ Syntax

```bash
cptd pack --export --output <folder>
cptd pack --import --from <folder> [--replace] [--skip-existing]
```

---

### 📤 Exporting Commands

```bash
cptd pack --export --output ./my_exports
```

* Creates a ZIP archive for each installed command
* Excludes internal folders like `__pycache__/` and `__pycache__.zip`
* Archive names match command names: `about.zip`, `cpdsl.zip`, etc.

---

### 📥 Importing Commands

```bash
cptd pack --import --from ./my_exports
```

* Installs all `.zip` files from the specified folder as CPTD commands
* Validates structure before installation

Additional flags:

* `--replace` — removes all current commands before installing new ones
* `--skip-existing` — skips already installed commands

---

### 🔐 Security

* Excludes unnecessary files: `__pycache__/`, `.pyc`, `.pyo`
* Rejects improperly structured commands
* Fully compatible with CPTD CLI’s security policy

---

### 🧪 Examples

```bash
# Export all commands to ZIP
cptd pack --export --output ./backup

# Import with removal of existing commands
cptd pack --import --from ./backup --replace

# Import only new commands
cptd pack --import --from ./shared --skip-existing
```

---

### 📁 Example Export Structure

```
my_exports/
├── about.zip
├── command.zip
├── pack.zip
├── cpdsl.zip
└── ...
```

---

### 📌 Compatibility

* ✔ Windows
* ✔ Linux
* ✔ macOS
* ✔ Offline mode

---

**`pack` is the bridge between the CLI and the community. Share commands, preserve your tools, and build the CPTD ecosystem.**
