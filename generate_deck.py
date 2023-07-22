import dataclasses

import generate_svgs

# https://www.albert.io/blog/amino-acid-study-guide-structure-and-function/


@dataclasses.dataclass
class AminoAcid:
    name: str
    three_letter_code: str
    one_letter_code: str


def generate_decks():
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


if __name__ == "__main__":
    generate_decks()
