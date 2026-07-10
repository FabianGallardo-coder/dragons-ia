## OpenWiki

This repository has documentation located in the /openwiki directory.

Start here:
- [OpenWiki quickstart](openwiki/quickstart.md)

OpenWiki includes repository overview, architecture notes, workflows, domain concepts, operations, integrations, testing guidance, and source maps.

When working in this repository, read the OpenWiki quickstart first, then follow its links to the relevant architecture, workflow, domain, operation, and testing notes.

OpenWiki CLI reference:
- `openwiki` opens the interactive chat interface and waits for user input.
- `openwiki "message"` sends a chat message immediately, then keeps the chat open.
- `openwiki --init [message]` initializes OpenWiki documentation for the current repository.
- `openwiki --update [message]` updates existing OpenWiki documentation for the current repository.
- `openwiki -p "message"` or `openwiki --print "message"` runs once, prints the final assistant output, and exits.
- `openwiki --modelId <id>` selects a model ID for that run.
- `openwiki --help` prints current usage, options, and examples.

If the user asks what the CLI can do, asks for commands/options/usage/examples, or asks for more details about OpenWiki itself, run `openwiki --help` with the available tools when possible and base your answer on the help output. If you cannot run the command, answer from the CLI reference above and say you could not verify live help output.