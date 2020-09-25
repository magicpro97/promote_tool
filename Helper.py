import os
import time
import re


def clear(): os.system('clear')


def __listHeight(driver, command):
    return driver.execute_script("return " + command)


def scroll_down(driver, command="document.body.scrollHeight", step=800):
    """A method for scrolling the page."""
    height_script = "return " + command

    # Get scroll height.
    scroll_height = __listHeight(driver, command)

    scroll_step = 0

    while True:
        # Scroll down to the bottom.
        driver.execute_script(
            "window.scrollTo(" + str(scroll_step) + "," + str(scroll_step + step) + ");")

        scroll_step += step

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        scroll_height = __listHeight(driver, command)

        if scroll_step >= scroll_height:
            break


def trim_indent(s: str):
    s = re.sub(r'^\n+', '', s)
    s = re.sub(r'\n+$', '', s)
    spaces = re.findall(r'^ +', s, flags=re.MULTILINE)
    if len(spaces) > 0 and len(re.findall(r'^[^\s]', s, flags=re.MULTILINE)) == 0:
        s = re.sub(r'^%s' % (min(spaces)), '', s, flags=re.MULTILINE)
    return s
