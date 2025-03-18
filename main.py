def getLocationInput():
    user_location = input("Please enter your current 5-digit Zipcode XXXXX\n-> ")
    if len(user_location) == 5 and user_location.isdigit():
        return user_location
    else:
        print(f"Supplied zipcode invalid length... {user_location}")
        retry = input("would you like to retry? (Y/n)")
        if retry.lower() == "y":
            return getLocationInput()
        else:
            print(f"Supplied zipcode invalid length... Maybe go outside to check the weather until I can implement search by city/state")
            return None

def main():
    print(getLocationInput())
    
if __name__ =="__main__":
    main()