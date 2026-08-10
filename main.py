import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from StreamDeck.Transport.Transport import TransportError

from spotipy.oauth2 import SpotifyOAuth
from spotipictl import SpotifyCtl  

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")

# spotify client
auth_manager = SpotifyOAuth(
    scope="user-modify-playback-state user-read-playback-state playlist-read-private",
    redirect_uri="https://suck_my_ball_mate:8004",
    open_browser=True,
)
sp_client = SpotifyCtl(auth_manager) 

# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):
    next_page_index = deck.key_count() - 1
    previous_page_index = 0

    if key == next_page_index:
        name = "next"
        icon = "{}.png".format("Next")
        font = "Roboto-Regular.ttf"
        label = "Next" if state else "Next"
    elif key == previous_page_index:
        name = "previous"
        icon = "{}.png".format("Previous")
        font = "Roboto-Regular.ttf"
        label = "Prev" if state else "Prev"
    else:
        name = "emoji"
        icon = "{}.png".format("Pressed" if state else "Released")
        font = "Roboto-Regular.ttf"
        label = "Pressed!" if state else "Key {}".format(key)

    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }

# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):
    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

    # Don't try to draw an image on a touch button
    if key >= deck.key_count():
        return

    # Update the key image based on the new key state.
    # update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        key_style = get_key_style(deck, key, state)

        #for i in key_style.items():
            #print(i)
        if key == 1:
            sp_client.next_track()

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        # This example only works with devices that have screens.
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        # Set initial screen brightness to 30%.
        deck.set_brightness(50)

        # Set initial key images.
        # for key in range(deck.key_count()):
            # update_key_image(deck, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except (TransportError, RuntimeError):
                pass
