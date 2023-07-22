import dataclasses
import enum
import os

import genanki

import generate_svgs

# https://www.albert.io/blog/amino-acid-study-guide-structure-and-function/


@dataclasses.dataclass
class AminoAcid:
    name: str
    three_letter_code: str
    one_letter_code: str


class NoteField(enum.StrEnum):
    NAME = "Name"
    STRUCTURE = "Structure"
    THREE_LETTER_CODE = "Three Letter Code"
    ONE_LETTER_CODE = "One Letter Code"


def generate_deck() -> None:
    AMINO_ACIDS = (
        AminoAcid("Alanine", "Ala", "A"),
        AminoAcid("Arginine", "Arg", "R"),
        AminoAcid("Asparagine", "Asn", "N"),
        AminoAcid("Aspartic acid", "Asp", "D"),
        AminoAcid("Cysteine", "Cys", "C"),
        AminoAcid("Glutamic acid", "Glu", "E"),
        AminoAcid("Glutamine", "Gln", "Q"),
        AminoAcid("Glycine", "Gly", "G"),
        AminoAcid("Histidine", "His", "H"),
        AminoAcid("Isoleucine", "Ile", "I"),
        AminoAcid("Leucine", "Leu", "L"),
        AminoAcid("Lysine", "Lys", "K"),
        AminoAcid("Methionine", "Met", "M"),
        AminoAcid("Phenylalanine", "Phe", "F"),
        AminoAcid("Proline", "Pro", "P"),
        AminoAcid("Selenocysteine", "Sec", "U"),
        AminoAcid("Serine", "Ser", "S"),
        AminoAcid("Threonine", "Thr", "T"),
        AminoAcid("Tryptophan", "Trp", "W"),
        AminoAcid("Tyrosine", "Tyr", "Y"),
        AminoAcid("Valine", "Val", "V"),
    )

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    OUT_DIR = os.path.join(BASE_DIR, "out")
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
        generate_svgs.generate_svgs((aa.name for aa in AMINO_ACIDS), OUT_DIR)

    MODEL = genanki.Model(
        1864258524,  # ID is unique, do not change
        "Amino Acids Model",
        fields=[{"name": member.value} for member in NoteField],
        templates=[
            template(NoteField.NAME, NoteField.STRUCTURE, BASE_DIR),
            template(NoteField.STRUCTURE, NoteField.NAME, BASE_DIR),
            template(NoteField.NAME, NoteField.THREE_LETTER_CODE, BASE_DIR),
            template(NoteField.THREE_LETTER_CODE, NoteField.NAME, BASE_DIR),
            template(NoteField.NAME, NoteField.ONE_LETTER_CODE, BASE_DIR),
            template(NoteField.ONE_LETTER_CODE, NoteField.NAME, BASE_DIR),
        ],
        css=open(os.path.join(BASE_DIR, "model.css")).read(),
    )

    DECK = genanki.Deck(1304768788, "Amino Acids")  # ID is unique, do not change

    for aa in AMINO_ACIDS:
        DECK.add_note(
            genanki.Note(
                model=MODEL,
                fields=[
                    aa.name,
                    f'<img src="{aa.name}.svg">',
                    aa.three_letter_code,
                    aa.one_letter_code,
                ],
            )
        )

    PACKAGE = genanki.Package(DECK)
    PACKAGE.media_files = (
        os.path.join(OUT_DIR, f"{aa.name}.svg") for aa in AMINO_ACIDS
    )
    PACKAGE.write_to_file("Amino_Acids.apkg")


def template(f1: NoteField, f2: NoteField, base_dir: str) -> dict[str, str]:
    front_path = os.path.join(
        base_dir, "html", f"{f1}-{f2}.front.html".replace(" ", "_")
    )

    back_path = os.path.join(base_dir, "html", f"{f1}-{f2}.back.html".replace(" ", "_"))
    if not os.path.exists(back_path):
        back_path = os.path.join(
            base_dir, "html", f"{f2}-{f1}.back.html".replace(" ", "_")
        )

    return {
        "name": f"{f1} -> {f2}",
        "qfmt": open(front_path).read(),
        "afmt": open(back_path).read(),
    }


if __name__ == "__main__":
    generate_deck()
