from progression import main_generation,major_roman,major_tonal_triad

import random
import subprocess
from PIL import Image
import os

def question_generation(ans_prograssion):
    options = []
    while len(options) < 5:
        bar=[]
        while len(bar) <4 :
            bar.append(random.choice(major_roman))
        if bar != ans_prograssion and bar not in options:
            options.append(bar)
        else:
            bar.clear()
    options.append(ans_prograssion)
    random.shuffle(options)
    correct_index = options.index(ans_prograssion)
    return correct_index,options


def display_options(options):
    cleaned_progressions = ['-'.join(progression) for progression in options]
    return cleaned_progressions


def format_melody(melody):
  formatted = []
  for note in melody:
      note = note.replace("'", "").replace(',', '').replace('[', '').replace(']', '')
      formatted.append(note)
  return ' '.join(formatted)

def key_signature(key="F-sharp minor"):
    letter,quality=key.split()
    if "sharp" in letter:
        accidental="s"
        letter=letter[0]
    elif "flat" in letter:
        accidental="f"
        letter=letter[0]
    else:
        accidental=""
    return f"{letter.lower()}{accidental} \{quality}"

def chord_accompany(key="C major",chords=["ii","IV","V","I"]):
    scale, triad_dic = major_tonal_triad(key)
    chord_progression = []
    for chord in chords:
        chord_notes = triad_dic[chord]
        chord_str = "<" + " ".join(chord_notes) + ">1"
        chord_progression.append(chord_str)
    return " ".join(chord_progression)

def lilypond_generation(melody, name, key,accompany):
    score_meldoy = []
    for bar in melody:
        score_meldoy.extend(bar)
    lilypond_score = f"""
\\version "2.22.0"  
\\header {{
  tagline = "" \\language "english"
}}

#(set-global-staff-size 26)
\\score {{

    \\fixed c' {{ 
    \\key {key_signature(key)}

      {format_melody(score_meldoy)}
      \\bar "|"
    }}
    \\layout {{
      indent = 0\\mm
      ragged-right = ##f
      \\context {{
        \\Score
        \\remove "Bar_number_engraver"
      }}
    }}
}}
\\score {{\\new StaffGroup <<
     \\new Staff \\fixed c' {{
      {format_melody(score_meldoy)}
      \\bar "|"
    }}
    \\new Staff \\fixed c {{
      {accompany}
      \\bar "|"
    }}>>
    \\midi {{ }}
}}
"""

    with open('score.ly', 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image and MIDI file
    subprocess.run(['lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300', f'--output=static/cropped_score_{name}', 'score.ly'],
                   check=True)

    return f'static/cropped_score_{name}.png'


def audio_generation():
    subprocess.run(['fluidsynth', '-ni', 'GeneralUser/Yamaha-Grand-Lite-SF-v1.1.sf2', 'static/cropped_score_question.midi', '-F', f'static/question.mp3', '-r', '44100'],
               check=True)
