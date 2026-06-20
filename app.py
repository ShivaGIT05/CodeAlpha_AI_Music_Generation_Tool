import streamlit as st
import numpy as np
from scipy.io.wavfile import write
import os
from datetime import datetime

st.set_page_config(
    page_title="AI Music Studio",
    page_icon="🎵"
)

SAVE_DIR = "generated_music"

os.makedirs(
    SAVE_DIR,
    exist_ok=True
)

styles = {

"Melody":[261,329,392,523],
"Romantic":[220,277,330,440],
"Mass":[130,196,261,392],
"Calm":[196,247,294,392],
"Happy":[262,330,392,494],
"Sad":[196,233,294,349],
"LoFi":[220,262,311,370],
"Electronic":[330,440,550,660]

}

st.title("🎵 AI Music Generation Studio")

style = st.selectbox(
"Choose Style",
list(styles.keys())
)

duration = st.slider(
"Duration",
5,
60,
15
)

generate = st.button(
"Generate Music"
)


def create_note(freq, sec):

    sr = 44100

    t = np.linspace(
        0,
        sec,
        int(sr*sec)
    )

    note = (

        0.6*np.sin(
            2*np.pi*freq*t
        )

        +

        0.3*np.sin(
            2*np.pi*freq*2*t
        )

        +

        0.2*np.sin(
            2*np.pi*freq*0.5*t
        )

    )

    fade = np.linspace(
        0,
        1,
        len(note)
    )

    return note*fade


if generate:

    sr = 44100

    song = np.array([])

    scale = styles[style]

    for i in range(duration*2):

        mode = np.random.choice([
            "melody",
            "chord",
            "bass"
        ])

        if mode == "melody":

            freq = np.random.choice(
                scale
            )

            segment = create_note(
                freq,
                0.5
            )

        elif mode == "chord":

            root = np.random.choice(
                scale[:-2]
            )

            segment = (

                create_note(
                    root,
                    0.5
                )

                +

                create_note(
                    root*1.25,
                    0.5
                )

                +

                create_note(
                    root*1.5,
                    0.5
                )

            )

        else:

            freq = np.random.choice(
                scale
            )/2

            segment = create_note(
                freq,
                0.5
            )

        song = np.concatenate(
            [
                song,
                segment
            ]
        )

    song = song/np.max(
        np.abs(song)
    )

    audio = np.int16(
        song*32767
    )

    filename = (

        style
        +

        "_"

        +

        datetime.now().strftime(
            "%H%M%S"
        )

        +

        ".wav"

    )

    path = os.path.join(
        SAVE_DIR,
        filename
    )

    write(
        path,
        sr,
        audio
    )

    st.success(
        "Music Generated!"
    )

    st.audio(
        path
    )

    with open(
        path,
        "rb"
    ) as f:

        st.download_button(
            "⬇ Download",
            f,
            filename
        )

st.subheader(
"Generated History"
)

for f in os.listdir(
SAVE_DIR
):

    st.write(
        "🎵",
        f
    )