import os
import re
import time
from typing import Iterable

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from AminoAcid import AminoAcid


def generate_svgs(amino_acids: Iterable[AminoAcid], xml_dir: str, out_dir: str) -> None:
    NAME_TO_STRUCTURE_SLEEP = 0.75
    GET_SVG_SLEEP = 0.5

    # Page initialization
    D = webdriver.Chrome()
    D.implicitly_wait(10)  # set implicit wait seconds
    D.get("https://chemdrawdirect.perkinelmer.cloud/js/sample/index.html?wasm=1")
    D.find_element(By.XPATH, "//button[text()='Allow']").click()

    is_first = True
    for aa in amino_acids:
        if aa.use_xml_to_svg:
            with open(os.path.join(xml_dir, f"{aa.name}.xml")) as F:
                pyperclip.copy(F.read())
            D.find_element(By.PARTIAL_LINK_TEXT, "Structure").click()
            D.find_element(By.LINK_TEXT, "Load CDXML").click()
            D.find_element(By.ID, "modalApiInputContent").send_keys(Keys.CONTROL, "v")
            D.find_element(By.ID, "btnAcceptInput").click()
        else:
            D.find_element(By.XPATH, "(//button[@id='CDW_NameToStructure'])[2]").click()
            if is_first:  # Disable "Paste name below structure" on first run
                D.find_element(By.CSS_SELECTOR, ".checkbox-inline").click()
                is_first = False
            input_field = D.find_element(
                By.CSS_SELECTOR, ".cdd-dialog-input:nth-child(2)"
            )
            input_field.clear()
            input_field.send_keys(aa.name)
            D.find_element(By.CSS_SELECTOR, ".cdd-button-ok").click()
            time.sleep(NAME_TO_STRUCTURE_SLEEP)

        D.find_element(By.LINK_TEXT, "Structure").click()
        D.find_element(By.LINK_TEXT, "Get SVG").click()
        time.sleep(GET_SVG_SLEEP)
        svg = D.find_element(By.ID, "modalApiResultContentText").text
        svg = modify_svg(svg)
        with open(os.path.join(out_dir, f"{aa.name}.svg"), "w") as F:
            F.write(svg)

        D.find_element(
            By.CSS_SELECTOR, ".modal-footer > .btn-default:nth-child(2)"
        ).click()  # Exit modal
        D.find_element(By.LINK_TEXT, "Document").click()
        D.find_element(By.LINK_TEXT, "Clear").click()


def modify_svg(svg: str) -> str:
    return (
        re.sub('width=".*px" height=".*px"', 'width="200px"', svg)
        .replace('style="background-color: #ffffffff"', "")
        .replace('fill="#000000"', 'fill="#ffffff"')
    )
