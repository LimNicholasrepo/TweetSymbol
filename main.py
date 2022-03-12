import tweepy
from datetime import date
import csv
import json
import yfinance as yf
import datetime
import time


def tweet(id):
    with open("API_credentials.csv", "r") as file_login:
        csv_pointer = csv.reader(file_login)
        for each in csv_pointer:
            if len(each) > 0:
                if id == each[0]:
                    API_key = each[1]
                    API_key_secret = each[2]
                    Access_Token = each[3]
                    Access_Token_Secret = each[4]
                else:
                    pass
            else:
                pass

    auth = tweepy.OAuth1UserHandler(API_key, API_key_secret)
    auth.set_access_token(Access_Token, Access_Token_Secret)
    api = tweepy.API(auth)

    screen_name = "@" + id

    # Retrieves stock symbol and deletes the tweet
    while True:
        for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items():
            id = status.id
            tickerSymbol = status.full_text
            try:
                # get data on this ticker
                tickerData = yf.Ticker(tickerSymbol)

                info = tickerData.info
                for k, v in info.items():
                    if v != None:
                        api.destroy_status(id)
                        # retrieve stock data
                        tickerDf = tickerData.history(
                            period='1d', start=date.today(), end=date.today())

                        # extract relevant data
                        High = tickerDf[0:1]["High"].to_numpy()[0]
                        Low = tickerDf[0:1]["Low"].to_numpy()[0]
                        Close = tickerDf[0:1]["Close"].to_numpy()[0]

                        # update feed with stock price information
                        api.update_status(
                            "Information on " + tickerSymbol + ":\nHigh is: "
                            + str(High) + "\nLow is: " + str(
                                Low) + "\nClose is: " + str(Close))
                        break
                    else:
                        break
                break

            except:
                break
        break


def credentials(id):
    data = []
    while True:
        API_key = str(input("Please input your API key: "))
        API_key_secret = str(input("Please input your API key secret: "))
        Access_Token = str(input("Please input your access token: "))
        Access_Token_Secret = str(input("Please input your access token secret: "))

        auth = tweepy.OAuth1UserHandler(API_key, API_key_secret)
        auth.set_access_token(Access_Token, Access_Token_Secret)
        api = tweepy.API(auth)

        try:
            api.update_status("Successfully connected")
            print("Verified!")
            api_list = [id, API_key, API_key_secret, Access_Token, Access_Token_Secret]
            data.append(api_list)
            with open("API_credentials.csv", "w") as file_login:
                csv_pointer = csv.writer(file_login)
                csv_pointer.writerows(data)
            break

        except ValueError:
            print(
                "Sorry it seems you entered the wrong credentials.")  # Checks to see if the tweet was able to be processed


def signup():
    data = []
    try:
        with open("login_credentials.csv", "r") as file_login:
            csv_pointer = csv.reader(file_login)
            for each in csv_pointer:
                # Check for empty list
                if len(each) > 0:
                    data.append(each[0])
                else:
                    pass
    except FileNotFoundError:
        pass
    while True:
        login = input("Please enter your twitter @: ")
        password = input("Please enter a password: ")
        if login not in data:
            credentials(login)
            cred = [login, password]
            data.append(cred)
            with open("login_credentials.csv", "w") as file_login:
                csv_pointer = csv.writer(file_login)
                csv_pointer.writerows(data)
                break
        else:
            print("Sorry the login credential already exists.")
            login = ""
            break
    return login


def login():
    # Login loop
    while True:
        # Request login credentials
        login = input("Please enter your twitter @: ")
        password = input("Please enter your password: ")

        with open("login_credentials.csv", "r") as file_login:
            csv_pointer = csv.reader(file_login)
            for each in csv_pointer:
                if len(each) > 0:
                    if login == each[0]:
                        if password == each[1]:
                            print("Valid Login!")
                            return login
                        else:
                            login = ""
                            print("Invalid login or password!")
                            return login
            login = ""
            return login

def main():
    while True:
        login_option = 0
        try:
            print("Welcome to stock request!\n 1. Login \n 2. Sign Up \n 3. Exit")
            login_option = int(input("Please enter the option number here: "))

        except ValueError:
            print("Please enter a number: ")

        if login_option == 1: # for login option
            try:
                with open("login_credentials.csv", "r") as file_login:
                    csv_pointer = csv.reader(file_login)
                flag = True
                while flag:
                    id = login()
                    if id == "":
                        while True:
                            user_input = input("Would you like to try again?(Y/N): ").upper()
                            if user_input == "Y":
                                break
                            elif user_input == "N":
                                flag = False
                                break
                            else:
                                print("Please enter a valid input! ")
                    else:
                        return id
            except FileNotFoundError:
                print("Please sign up first!\n")

        elif login_option == 2: # for sign up option
            flag = True
            while flag:
                # return id after user create an account
                id = signup()

                if id == "":
                    while True:
                        user_input = input("Would you like to try again?(Y/N): ").upper()
                        if user_input == "Y":
                            break
                        elif user_input == "N":
                            flag = False
                            break
                        else:
                            print("Please enter a valid input! ")

                else:
                    return id

        elif login_option == 3:
            # Exit code
            break

        else:
            print("Please enter a valid option! ")
        break

id = main()
print("You may start requesting stock prices!")
while True:
    tweet(id)
    time.sleep(10)
#tweet(API_key, API_key_secret, Access_Token, Access_Token_Secret)
#API_key, API_key_secret, Access_Token, Access_Token_Secret = credentials()