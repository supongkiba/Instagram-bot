from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from time import sleep

class InstaBot():
    def __init__(self, uName, pWord):
        self.uName = uName 
        self.pWord = pWord
        self.driver = webdriver.Chrome()
        self.following = []
        self.followers = []


    def mainMenu(self):
        action = input("\nFollowers or Unfollowers?(F/U). Press q Key to Exit. \n")
        if action.lower() == "u" or action.lower() == "unfollowers":
            self.unFollow()
        elif action.lower() == "f" or action.lower() == "followers":
            self.follow()
        elif action.lower() == "q":
            sys.exit()
        else:
            print("Sorry, I didn't get you! ")
            self.mainMenu()


    def continueMenu(self):
        cont = input("\nDo you wanna go back to the main menu? (Yes/No)")
        if cont.lower() == "yes" or cont.lower() == "y":
            self.mainMenu()
        elif cont.lower() == "no" or cont.lower() == "n":
            sys.exit()
        else:
            print("Sorry, I didn't get you!\n")
            self.continueMenu()


    def getNames(self):
        """Function to retieve a list of following/followers usernames. 
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
                self.driver.get('https://www.instagram.com/' + user)
                sleep(2)
                if category == "unfollow":
                    self.driver.find_elements_by_xpath('//button')[1].click()
                    sleep(1)
                    self.driver.find_element_by_xpath("//*[text()='Unfollow']").click()
                    print("\nUnfollowed " + user + "...\n")
                else:
                    try:
                        self.driver.find_element_by_xpath("//*[text()='Follow']").click()
                        print("\nFollowed " + user + "\n")
                    except:
                        self.driver.find_element_by_xpath("//button[text()='Follow Back']").click()
                        print("\nFollowed back " + user + "\n")
                sleep(1)
            except:
                print("\nSomthing went wrong! Please make sure the username '" + user + "' and xPath are correct.")


    def unFollow(self):
        not_following_back = [user for user in self.following if user not in self.followers]
        print("\nThese Users are not Following you back\n\n" + ', '.join(not_following_back) + "\n\n")
        action = input("\nDo you wanna UNFOLLOW all of them? (Yes/NO).\n-Press m to go back to the main Menu\n-Press q to Exit\n")
        if action.lower() == "yes" or action.lower() == "y":
            self.instaAction(not_following_back, "unfollow")
            self.continueMenu()
        elif action.lower() == "no" or action.lower() == "n":
            userToUnfollow = input("\nPlease enter comma separated usernames to Unfollow.\n-Press m to go back to the main Menu\n-Press q to exit\n")
            if userToUnfollow.lower() == "q":
                sys.exit()
            elif userToUnfollow.lower() == "m":
                self.mainMenu()
            else:
                self.instaAction(userToUnfollow.replace(" ", "").split(','), "unfollow")
                self.continueMenu()
        elif action.lower() == "m":
            self.mainMenu()
        elif action.lower() == "q":
            sys.exit()
        else:
            print("Sorry, I didn't get you! ")
            self.unFollow()


    def follow(self):
        iam_not_following = [user for user in self.followers if user not in self.following]
        print("\nYou're not Following back these Followers!\n\n" + ', '.join(iam_not_following) + "\n\n")
        action = input("\nDo you wanna FOLLOW all of them? (Yes/NO).\n-Press m to go back to the main Menu\n-Press q to exit\n")
        if action.lower() == "yes" or action.lower() == "y":
            self.instaAction(iam_not_following, "follow")
            self.continueMenu()
        elif action.lower() == "no" or action.lower() == "n":
            userToFollow = input("\nPlease enter comma separated usernames to Follow.\n-Press m to go back to the main Menu\n-Press q to exit\n")
            if userToFollow.lower() == "q":
                sys.exit() 
            elif userToFollow.lower() == "m":
                self.mainMenu()
            else:
                self.instaAction(userToFollow.replace(" ", "").split(','), "follow")
                self.continueMenu()
        elif action.lower() == "m":
            self.mainMenu()
        elif action.lower() == "q":
            sys.exit()
        else:
            print("Sorry, I didn't get you! ")
            self.follow()


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
            print("\nLogging in to Instagram...\n")
            sleep(3)

            try:
                notnow = self.driver.find_element_by_xpath("//button[text()='Not Now']")
                notnow.click()
            except:
                pass

            self.driver.get('https://www.instagram.com/' + self.uName)

            sleep(2)
            
            print("\nScanning the Following and Followers list. This may take sometime, sit back and relax!\n")
            print("### PLEASE DO NOT INTERACT WITH THE BROWSER ###\n\n")
            self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
            print("Fetching the 'Following' list...\n")
            self.following = self.getNames()
            
            self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
            print("Fetching the 'Followers' list...\n")
            self.followers = self.getNames()

            self.mainMenu()
            self.continueMenu()


bot = InstaBot("supong__", "LOngkok!@14")
bot.initiateBot()