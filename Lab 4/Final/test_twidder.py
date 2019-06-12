from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By


'''
Requirements to prove:
    1. Sign up
    2. Sign in
    3. Post comment in user wall
    4. Refresh user comments wall
    5. Sign out
'''

#Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path='./chromedriver')

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

WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "textSignUp"), "Successfully sign up")) #Wait untill sign up user 

print(driver.find_element_by_id("textSignUp").get_attribute('innerHTML'))

#Sign in
print("Sign in")

email = driver.find_element_by_id("emailLogIn")
email.send_keys("serga155@student.liu.se")

password = driver.find_element_by_id("passwordLogIn")
password.send_keys("12345678")

driver.find_element_by_id("buttonSignIn").click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "homePanel"))) #Wait untill home panel is displayed

print("currentView: ", driver.execute_script('return currentView'))

#Post comment in user wall
print("Post comment in user wall")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userCommentBox"))) #Wait untill userCommentBox is displayed

post_comment_wall = driver.find_element_by_id("userCommentBox")
post_comment_wall.send_keys("I am posting a comment through Selenium")
driver.find_element_by_id("buttonUserPostComment").click()
 
WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "resultText"), "Message posted")) #Wait untill messsage is posted 

print("Post comment status: " , driver.find_element_by_id("resultText").get_attribute('innerHTML'))

#Change password
print("Change password")

driver.find_element_by_id("accountButton").click()

current_password = driver.find_element_by_id("currentPassword")
current_password.send_keys("12345678")

new_password = driver.find_element_by_id("newPassword")
new_password.send_keys("123456789")

repeat_password = driver.find_element_by_id("repeatNewPassword")
repeat_password.send_keys("123456789")

driver.find_element_by_id("buttonChangePassword").click()

WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "changePasswordResultText"), "Successfully changed password")) #Wait untill password is changed 

print("Change password status: " , driver.find_element_by_id("changePasswordResultText").get_attribute('innerHTML'))

#Sign out
print("Sign out")

driver.find_element_by_id("accountButton").click()

driver.find_element_by_id("buttonSignOut").click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "welcomeView"))) #Wait untill welcome view is displayed

print("currentView: ", driver.execute_script('return currentView'))

#Test finish
print("Test finish")
driver.quit()

