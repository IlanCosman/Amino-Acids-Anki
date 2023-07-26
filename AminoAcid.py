import dataclasses


@dataclasses.dataclass
class AminoAcid:
    name: str
    three_letter_code: str
    one_letter_code: str
    use_xml_to_svg: bool = False
