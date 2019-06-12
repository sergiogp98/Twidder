from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

'''
Requirements to prove:
    1. Sign up
    2. Sign in
    3. Post comment in user wall
    4. Refresh user comments wall
    5. Sign out
'''

#Create a new instance of the Chrome driver
driver = webdriver.Chrome('/home/sergiogp98/Escritorio/Lab 4 Selenium/chromedriver')

#Go to the Twidder welcome page
driver.get("http://localhost:5000")
driver.get("http://localhost:5000")
print(driver.title)

#Sign up
print("Sign up")

first_name = driver.find_element_by_id("firstName")
first_name.send_keys("Sergio")

family_name = driver.find_element_by_id("familyName")
family_name.send_keys("Garcia Prados")

city = driver.find_element_by_id("city")
city.send_keys("Granada")

country = driver.find_element_by_id("country")
country.send_keys("Spain")

email = driver.find_element_by_id("emailSignUp")
email.send_keys("serga155@student.liu.se")

password = driver.find_element_by_id("passwordSignUp")
password.send_keys("12345678")

repeat_password = driver.find_element_by_id("repeatPassword")
repeat_password.send_keys("12345678")

driver.find_element_by_id("buttonSignUp").click()

#Sign in
print("Sign in")

email = driver.find_element_by_id("emailLogIn")
email.send_keys("serga155@student.liu.se")

password = driver.find_element_by_id("passwordLogIn")
password.send_keys("12345678")

driver.find_element_by_id("buttonSignIn").click()

#Post comment in user wall
print("Post comment in user wall")
'''
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userCommentBox")))
finally:
    driver.quit()
'''
driver.implicitly_wait(10) # Wait untill "userCommentBox" is available
post_comment_wall = driver.find_element_by_id("userCommentBox")
post_comment_wall.send_keys("I am posting a comment through Selenium")
driver.find_element_by_id("buttonUserPostComment").click()

#Refresh user comments wall
print("Refresh user comments wall")

driver.find_element_by_id("buttonUserRefreshWall").click()

#Sign out
driver.find_element_by_id("accountButton").click()
driver.find_element_by_id("buttonSignOut").click()

#Test finish
print("Test finish")
driver.quit()

