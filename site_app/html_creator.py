import dominate.tags as tag 
import dominate
from dominate import util
import hikari
import os 
import secrets

url_map = {
    "Invite Bot": "https://discord.com/api/oauth2/authorize?client_id=979906554188939264&permissions=516020358208&scope=bot%20applications.commands",
    "Support Server" : "https://discord.com/invite/FyEE54u9GF"
}

def create_user_profile_tag(user:hikari.OwnUser=None ) -> str :
    doc = dominate.document(f"{user} | Dashboard")

    with doc.head:
        tag.link(rel='stylesheet', href='../static/profile.css')
    
    with doc:
        tag.body(background="../assets/backgrounds/"+secrets.choice(os.listdir('assets/backgrounds')))
          
        with tag.div(_class="header",id='main_page_header').add(tag.ol()):
            tag.a("Logout",id="header_link_buttons", _class="session_button", href=f"../logout/{user.id}")
            for item, url in url_map.items():
                tag.a(item,href=url,id="header_link_buttons" )
            tag.br();tag.br() ; tag.br()
        with tag.div(style="float: right;font-family: Rockwell Extra Bold, Rockwell Bold, monospace;", _class="profile_slot"):
            tag.img(src=user.display_avatar_url.url, _class="profile_image") 
            tag.br();tag.br()
            util.text(f"User tag: {user}")
            tag.br()
            util.text(f"User ID: {user.id}");tag.br()
            util.text(f"Created on: {user.created_at.strftime('%d-%B-%y')}")
            
    return str(doc).replace(
"""
  <body>
    <body background="../assets/backgrounds/bg_image2.png"></body>
""","<body background=\"../assets/backgrounds/bg_image2.png\">"
    ).replace(
"""
  <body>
    <body background="../assets/backgrounds/bg_image1.png"></body>
""","<body background=\"../assets/backgrounds/bg_image1.png\">"
    )
