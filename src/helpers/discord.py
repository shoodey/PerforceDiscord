import requests

from helpers.misc import count_file_operations


def post_embed(url, data):
    operations = count_file_operations(data["files"])

    message = {
        "username": "Perforce",
        "avatar_url": "https://cdn.discordapp.com/avatars/1218724189645574204/761b67d381803deeea83af683cd33af2.png?size=512",
        "embeds": [
            {
                "title": f"{data['author']} submitted revision #{data['revision_number']}",
                "color": "701425",
                "fields": [
                    {"name": "", "value": "\n".join(data["message"]), "inline": False}
                ],
                "footer": {
                    "text": f"🗃️{len(data['files'])} ✅{operations['add']} ✏️{operations['edit']} ❌{operations['delete']}"
                },
            }
        ],
    }
    requests.post(url, json=message)
