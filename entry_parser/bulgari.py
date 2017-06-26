# coding: utf-8

import sys
sys.path.append('../')
import util

prefix = 'www.bulgari.com'

def parse(driver, url):
    products = []
    driver.get(url)
    while True:
        elements = util.find_elements_by_css_selector(driver, 'a.bul-btn-more')
        cont = False
        for element in elements:
            if element.is_displayed():
                cont = True
                driver.execute_script('arguments[0].click();', element)
                util.sleep(3)
        if not cont:
            break
    elements = util.find_elements_by_css_selector(driver, 'a.product-link')
    for element in elements:
        products.append(element.get_attribute('href').strip())
    return ';'.join(products)
    
if __name__ == '__main__':
    print(parse(util.create_chrome_driver(), sys.argv[1]))
