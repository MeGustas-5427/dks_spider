# coding: utf-8

# 在Selenium Chrom里元素的css定位居然普通浏览器不同，不解。。。

import sys
sys.path.append('../')
import util

brand = 'balenciaga'
prefixes = ['www.balenciaga.cn']

def get_title(driver):
    title = ''
    element = util.find_element_by_css_selector(driver, 'h1.seo-only > div.modelName > span.modelName')
    if not element:
        raise Exception('Title not found for %s' % driver.current_url)
    else:
        title = element.text
        element = util.find_element_by_css_selector(driver, 'div.EditorialDescription > span.value')
        if element:
            title += ' - ' + element.text.strip()
    return title
    
def get_code(driver):
    return ''
    
def get_price(driver):
    price = 0
    # 先找折扣价
    element = util.find_element_by_css_selector(driver, 'div.item-main.bottom-content > div.priceUpdater > span.discounted.price > span.value')
    if not element: # 没有折扣就查看原价
        element = util.find_element_by_css_selector(driver, 'div.item-main.bottom-content > div > span.price > span.value')
    if element:
        text = element.text.strip()
        price = float(text.replace(',', '')) if text else 0
    return price
    
def get_intro(driver):
    intro = ''
    element = util.find_element_by_css_selector(driver, 'div[data-accordionpanel=item_detail] > span.icon-plus')
    if element:
        element.click()
    texts = []
    elements = util.find_elements_by_css_selector(driver, 'div.item-description > ul > li > span.value')
    for element in elements:
        texts.append(element.text.strip())
    if texts:
        intro = '\n'.join(texts)
    return intro
    
def get_images(driver):
    images = ''
    texts = set([])
    elements = util.find_elements_by_css_selector(driver, '#ItemSlideshowViewport > div.bx-wrapper > div.bx-viewport > ul > li > img')
    for element in elements:
        image = ((element.get_attribute('srcset').split(','))[0].split(' '))[0].strip()
        texts.add(image)
    images = ';'.join(texts)
    return images

def parse(driver, url):
    driver.get(url)
    good = {'brand':brand}
    good['title'] = get_title(driver)
    good['code'] = get_code(driver)
    good['price'] = get_price(driver)
    good['intro'] = get_intro(driver)
    good['images'] = get_images(driver)
    return good

if __name__ == '__main__':
    driver = util.create_chrome_driver()
    print(parse(driver, sys.argv[1]))
    driver.quit()
