import dataclasses
import enum

import genanki

import generate_svgs

# https://www.albert.io/blog/amino-acid-study-guide-structure-and-function/


@dataclasses.dataclass
class AminoAcid:
    name: str
    three_letter_code: str
    one_letter_code: str


class AminoAcidCardField(enum.StrEnum):
    NAME = "Name"
    STRUCTURE = "Structure"
    THREE_LETTER_CODE = "Three Letter Code"
    ONE_LETTER_CODE = "One Letter Code"


def generate_decks() -> None:
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

    generate_svgs.generate_svgs(aa.name for aa in AMINO_ACIDS)

    MODEL = genanki.Model(
        1864258524,  # ID is unique, do not change
        "Amino Acids Model",
        fields=[
            {"name": AminoAcidCardField.NAME},
            {"name": AminoAcidCardField.STRUCTURE},
            {"name": AminoAcidCardField.THREE_LETTER_CODE},
            {"name": AminoAcidCardField.ONE_LETTER_CODE},
        ],
        templates=[
            template(AminoAcidCardField.NAME, AminoAcidCardField.STRUCTURE),
            template(AminoAcidCardField.STRUCTURE, AminoAcidCardField.NAME),
            template(AminoAcidCardField.NAME, AminoAcidCardField.THREE_LETTER_CODE),
            template(AminoAcidCardField.THREE_LETTER_CODE, AminoAcidCardField.NAME),
            template(AminoAcidCardField.NAME, AminoAcidCardField.ONE_LETTER_CODE),
            template(AminoAcidCardField.ONE_LETTER_CODE, AminoAcidCardField.NAME),
        ],
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

    genanki.Package(DECK).write_to_file("out.apkg")


def template(f1: AminoAcidCardField, f2: AminoAcidCardField) -> dict[str, str]:
    return {
        "name": f"{f1} -> {f2}",
        "qfmt": f"{{{f1}}}",
        "afmt": f"{{FrontSide}}<hr id=answer>{{{f2}}}",
    }


if __name__ == "__main__":
    generate_decks()
