import sys

from dotenv import load_dotenv

from helpers.discord import post_embed
from helpers.misc import ensure_env_var
from helpers.revision import describe_revision, parse_description

load_dotenv()
discord_webhook_url = ensure_env_var("DISCORD_WEBHOOK_URL")

if len(sys.argv) < 2:
    raise ValueError("Revision number is missing")
revision_number = sys.argv[1]
if not revision_number.isdigit():
    raise ValueError("Revision number must be an integer")

revision_description = describe_revision(revision_number)
parsed_revision_description = parse_description(revision_description)

post_embed(discord_webhook_url, parsed_revision_description)
