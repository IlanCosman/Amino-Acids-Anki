import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def main() -> None:
    AMINO_ACID_NAMES = [
        "Alanine",
        "Arginine",
        "Asparagine",
    ]

    NAME_TO_STRUCTURE_SLEEP = 0.75
    GET_SVG_SLEEP = 0.5

    OUT_DIR = os.path.join(os.getcwd(), "out")
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    # Page initialization
    D = webdriver.Chrome()
    D.implicitly_wait(10)  # set implicit wait seconds
    D.get("https://chemdrawdirect.perkinelmer.cloud/js/sample/index.html?wasm=1")
    D.find_element(By.XPATH, "//button[text()='Allow']").click()

    is_first = True

    for name in AMINO_ACID_NAMES:
        D.find_element(By.XPATH, "(//button[@id='CDW_NameToStructure'])[2]").click()
        if is_first:
            D.find_element(By.CSS_SELECTOR, ".checkbox-inline").click()
            is_first = False
        D.find_element(By.CSS_SELECTOR, ".cdd-dialog-input:nth-child(2)").clear()
        D.find_element(By.CSS_SELECTOR, ".cdd-dialog-input:nth-child(2)").send_keys(
            name
        )
        D.find_element(By.CSS_SELECTOR, ".cdd-button-ok").click()
        time.sleep(NAME_TO_STRUCTURE_SLEEP)

        D.find_element(By.LINK_TEXT, "Structure").click()
        D.find_element(By.LINK_TEXT, "Get SVG").click()
        time.sleep(GET_SVG_SLEEP)
        svg = D.find_element(By.ID, "modalApiResultContentText").text
        svg = modify_svg(svg)
        with open(os.path.join(OUT_DIR, f"{name}.svg"), "w") as F:
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


if __name__ == "__main__":
    main()