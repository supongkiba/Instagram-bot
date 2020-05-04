import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class InstaBot():
    def __init__(self, uName, pWord):
        self.uName = uName 
        self.pWord = pWord
        self.driver = webdriver.Chrome()
        self.following = []
        self.followers = []


    def mainMenu(self):
        print("   ++++++++MENU+++++++++++   ")
        action = input("\n1)Press F to Follow back your Followers.\n2)Press U to Unfollow your Unfollowers.\n3)Press L to like all the Posts of an Account/#Hashtag.\n -Press q Key to Exit. \n").lower()
        if action == "u" or action == "unfollow":
            self.followOrUnfollow('unfollow')
        elif action == "f" or action == "follow":
            self.followOrUnfollow('follow')
        elif action == "l" or action == "like":
            self.likePosts()
        elif action == "q":
            sys.exit()
        else:
            print("\nSorry, I didn't get you! ")
            self.mainMenu()


    def continueMenu(self):
        cont = input("\nDo you wanna go back to the main menu? (Yes/No)").lower()
        if cont == "yes" or cont == "y":
            self.mainMenu()
        elif cont == "no" or cont == "n":
            sys.exit()
        else:
            print("\nSorry, I didn't get you!\n")
            self.continueMenu()


    def scanFollowingFollowers(self):
        self.driver.get('https://www.instagram.com/' + self.uName)

        sleep(2)

        print("""\nScanning the Following and Followers list. This may take sometime, sit back and relax!\n
              ### PLEASE DO NOT INTERACT WITH THE BROWSER ###\n\n""")
        
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()            
        print("Fetching the 'Following' list...\n")
        self.following = self.getNames()
            
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        print("Fetching the 'Followers' list...\n")
        self.followers = self.getNames()


    def getNames(self):
        """Function to retrieve a list of following/followers usernames. 
        Scrolls the follwing/followers element until it's loaded completely.
        This process is slow(intentionally) to make sure that all the users are captured.
        """
        sleep(1)
        scroll_box = self.driver.find_element_by_xpath("//*[@class='isgrP']")
        last_ht, ht = 0, 1
        # Scroll untill it lazy loads the complete list.
        while last_ht != ht:
            last_ht = ht
            sleep(3)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        sleep(1)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        try:
            self.driver.find_elements_by_xpath("//button")[3].click()
        except:
            self.driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div[2]/button").click()
        return names


    def instaAction(self, users, category):
        """Fucntion to follow/unfollow users
        """
        for user in users:
            try:
                self.driver.get(f'https://www.instagram.com/{user}')
                sleep(2)
                if category == "unfollow":
                    self.driver.find_elements_by_xpath('//button')[1].click()
                    sleep(1)
                    self.driver.find_element_by_xpath("//*[text()='Unfollow']").click()
                    print(f'\nUnfollowed {user}...\n')
                else:
                    try:
                        self.driver.find_element_by_xpath("//*[text()='Follow']").click()
                        print(f'\nFollowed {user}\n')
                    except:
                        self.driver.find_element_by_xpath("//button[text()='Follow Back']").click()
                        print(f'\nFollowed back {user}\n')
                sleep(1)
            except:
                print(f'\nSomthing went wrong! Please make sure the username "{user}" and xPath are correct.')


    def followOrUnfollow(self, category):
        if not self.following and not self.followers:
            self.scanFollowingFollowers()

        if category == "follow":
            accounts = [user for user in self.followers if user not in self.following]
            statement = "You're not Following back these Followers."
        else:
            accounts = [user for user in self.following if user not in self.followers]
            statement = "These Users are not Following you back"
            
        print(f'{statement}\n\n{", ".join(accounts)}\n')
        action = input(f'Do you wanna {category.upper()} all of them? (Yes/NO).\n-Press m to go back to the main Menu\n-Press q to Exit\n').lower()
        if action == "yes" or action == "y":
            self.instaAction(accounts, category)
            self.continueMenu()
        elif action == "no" or action == "n":
            inputVal = input(f'Please enter comma separated usernames to {category}.\n-Press m to go back to the main Menu\n-Press q to exit\n').lower()
            if inputVal == "q":
                sys.exit()
            elif inputVal == "m":
                self.mainMenu()
            else:
                self.instaAction(inputVal.replace(" ", "").split(','), "unfollow")
                self.continueMenu()
        elif action == "m":
            self.mainMenu()
        elif action == "q":
            sys.exit()
        else:
            print("\nSorry, I didn't get you!\n")
            self.followOrUnfollow(category)


    def likePosts(self):
        """
        Function to like all the posts of a User/Hashtag untill.
        """
        nextImg = True
        userHash = input("\nEnter a Username or a #Hashtag to like all the Posts\n-Press m to go back to the main Menu\n-Press q to exit\n").lower()
        if userHash == "q":
            sys.exit() 
        elif userHash == "m":
            self.mainMenu()
        else:
            url = "https://www.instagram.com/explore/tags/" if userHash[0] == "#" else "https://www.instagram.com/"
            self.driver.get(f'{url}{userHash.replace("#","")}')
            try: 
                self.driver.find_elements_by_xpath("//*[@class='v1Nh3 kIKUG  _bz0w']/a")[0].click()
                sleep(1)
                print(f'Liking all the Posts of {userHash}. Press close(X) in the browser to stop liking\n')
                # Don't click if it's already liked.
                if self.driver.execute_script('return document.getElementsByClassName("wpO6b ")[1].firstElementChild.getAttribute("aria-label")').lower() == "like":
                    self.driver.find_elements_by_xpath('//button[@class="wpO6b "]')[1].click()
                sleep(1)
                while nextImg:
                    try: 
                        self.driver.find_element_by_xpath('//*[text()="Next"]').click()
                        sleep(2)
                        if self.driver.execute_script('return document.getElementsByClassName("wpO6b ")[1].firstElementChild.getAttribute("aria-label")').lower() == "like":
                            self.driver.find_elements_by_xpath('//button[@class="wpO6b "]')[1].click()
                    except:
                        nextImg = False
                        print("Completed liking photos.\n")
            except: 
                print(f'Something went wrong. Please make sure "{userHash}" is a valid Username or a #Hashtag.')
                  


    def initiateBot(self): 
            print("\nOpening Instagram...\n")
            self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

            sleep(2)

            username = self.driver.find_element_by_name('username')
            username.send_keys(self.uName)
            password = self.driver.find_element_by_name('password')
            password.send_keys(self.pWord)

            try:
                button_login = self.driver.find_element_by_xpath("//button[@type='submit']")
            except:
                button_login = self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[6]/button/div')
            button_login.click()
            print("Logging in to Instagram...\n")
            sleep(3)

            try:
                notnow = self.driver.find_element_by_xpath("//button[text()='Not Now']")
                notnow.click()
            except:
                pass
            
            self.mainMenu()
            
            self.continueMenu()


bot = InstaBot("<username>", "<password>")
bot.initiateBot()