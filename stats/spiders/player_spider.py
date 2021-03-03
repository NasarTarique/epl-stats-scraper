import scrapy
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from ..items  import StatsItem


class playerspider(scrapy.Spider):
    name = "players"
    
    def start_requests(self):
        url = "https://www.premierleague.com/players/"
        yield scrapy.Request(url)

    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get("https://fantasy.premierleague.com/statistics")
        try:
            next_page_enabled = True
            while(next_page_enabled):
                buttons = driver.find_elements_by_xpath("/html/body/main/div/div[2]/div/div[1]/table/tbody/tr/td[1]/button")
                for button in buttons:
                    button.click()
                    player  = StatsItem()
                    for i in range(1,3,1):
                      try:
                          closebutton = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[1]/div/button")
                          name = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/div[1]/div/div[1]/h2")
                          pos = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/div[1]/div/div[1]/span")
                          team = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/div[1]/div/div[1]/div")
                          img  = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/div[1]/div/div[2]/img")
                          imgurl = [ img.get_attribute('src') ]
                          price = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/ul/li[4]/div")
                          form  = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/ul/li[1]/div")
                          totalpoints  = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/ul/li[3]/div")
                          ictrank  = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/div[2]/div[2]/div[2]/div/div/strong")
                          ictindexpos = driver.find_element_by_xpath(f"/html/body/div/div/dialog/div/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[4]/div/strong")
                          print("reached this")
                          player["name"] = name.text
                          player["position"] = pos.text
                          player["team"] = team.text
                          player["price"] = price.text
                          player["image_urls"] = imgurl
                          player["form"] = form.text
                          player["totalpoints"] = totalpoints.text
                          player["ictrank"] = ictrank.text
                          player["ictindexpos"] = ictindexpos.text
                          print("reached here :")
                          gwlist = WebDriverWait(driver,60).until(EC.visibility_of_all_elements_located((By.XPATH,f"/html/body/div/div/dialog/div/div[2]/div[{i+1}]/div/div/div[1]/div/table/tbody/tr")))

                          gameweekdata = []
                          for x in range(1,len(gwlist)+1):
                              xp = f"/html/body/div/div/dialog/div/div[2]/div[{i+1}]/div/div/div[1]/div/table/tbody/tr[{x}]"
                              gameweek = {
                                  "gw": driver.find_element_by_xpath(f"{xp}/td[1]").text,
                                  "pts":driver.find_element_by_xpath(f"{xp}/td[3]").text,
                                  "min played":driver.find_element_by_xpath(f"{xp}/td[4]").text,
                                  "goalscored":driver.find_element_by_xpath(f"{xp}/td[5]").text,
                                  "assists":driver.find_element_by_xpath(f"{xp}/td[6]").text,
                                  "clean sheet":driver.find_element_by_xpath(f"{xp}/td[7]").text,
                                  "goals conceded":driver.find_element_by_xpath(f"{xp}/td[8]").text,
                                  "own goals":driver.find_element_by_xpath(f"{xp}/td[9]").text,
                                  "penalties saved":driver.find_element_by_xpath(f"{xp}/td[10]").text,
                                  "penalties missed":driver.find_element_by_xpath(f"{xp}/td[11]").text,
                                  "yellow cards":driver.find_element_by_xpath(f"{xp}/td[12]").text,
                                  "red cards":driver.find_element_by_xpath(f"{xp}/td[13]").text,
                                  "saves":driver.find_element_by_xpath(f"{xp}/td[14]").text,
                                  "bonus":driver.find_element_by_xpath(f"{xp}/td[15]").text,
                                  "bps":driver.find_element_by_xpath(f"{xp}/td[16]").text,
                                  "influence":driver.find_element_by_xpath(f"{xp}/td[17]").text,
                                  "creativity":driver.find_element_by_xpath(f"{xp}/td[18]").text,
                                  "threat":driver.find_element_by_xpath(f"{xp}/td[19]").text,
                                  "ictindex":driver.find_element_by_xpath(f"{xp}/td[20]").text
                              }
                              gameweekdata.append(gameweek) 
                          player["gameweekdata"] = gameweekdata

                          prevseasondata = []
                          try:
                              prevlist = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH,f"/html/body/div/div/dialog/div/div[2]/div[{i+1}]/div/div/div[3]/div/table/tbody/tr")))
                              for x in range(1,len(prevlist)+1):
                                  xp = f"/html/body/div/div/dialog/div/div[2]/div[{i+1}]/div/div/div[3]/div/table/tbody/tr[{x}]"
                                  prevseason = {
                                      "season":driver.find_element_by_xpath(f"{xp}/td[1]").text,
                                      "pts":driver.find_element_by_xpath(f"{xp}/td[2]").text,
                                      "min played":driver.find_element_by_xpath(f"{xp}/td[3]").text,
                                      "goalscored":driver.find_element_by_xpath(f"{xp}/td[4]").text,
                                      "assists":driver.find_element_by_xpath(f"{xp}/td[5]").text,
                                      "clean sheet":driver.find_element_by_xpath(f"{xp}/td[6]").text,
                                      "goals conceded":driver.find_element_by_xpath(f"{xp}/td[7]").text,
                                      "own goals":driver.find_element_by_xpath(f"{xp}/td[8]").text,
                                      "penalties saved":driver.find_element_by_xpath(f"{xp}/td[9]").text,
                                      "penalties missed":driver.find_element_by_xpath(f"{xp}/td[10]").text,
                                      "yellow cards":driver.find_element_by_xpath(f"{xp}/td[11]").text,
                                      "red cards":driver.find_element_by_xpath(f"{xp}/td[12]").text,
                                      "saves":driver.find_element_by_xpath(f"{xp}/td[13]").text,
                                      "bonus":driver.find_element_by_xpath(f"{xp}/td[14]").text,
                                      "bps":driver.find_element_by_xpath(f"{xp}/td[15]").text,
                                      "influence":driver.find_element_by_xpath(f"{xp}/td[16]").text,
                                      "creativity":driver.find_element_by_xpath(f"{xp}/td[17]").text,
                                      "threat":driver.find_element_by_xpath(f"{xp}/td[18]").text,
                                      "ictindex":driver.find_element_by_xpath(f"{xp}/td[19]").text
                                  }
                                  prevseasondata.append(prevseason)
                              player["prevseason"] = prevseasondata
                          except Exception as e:
                              print("An Exception has occurred")
                              print(e)
                          closebutton.click() 
                          break
                      except Exception as e:
                          print("Exception Occured")
                          print(e)
                    yield player
                next_page = driver.find_element_by_xpath("/html/body/main/div/div[2]/div/div[1]/div[3]/button[3]")
                next_page_enabled = next_page.is_enabled()
                if(next_page_enabled):
                    next_page.click()
        except Exception as e:
            print("Exception occurred")
            print(e)
