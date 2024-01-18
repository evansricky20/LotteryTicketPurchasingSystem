import random
from datetime import datetime


# Lottery Ticket Purchasing System
# This program uses textfile databases that in specific formats
# TicketDetails.txt, database.txt, admindatabase.txt, PreviousWinningNumbers.txt,
# UserPurchases.txt, and WinningNumbers.txt need to be in the same directory as program.
# System uses keyboard input


# createAccount function
# Takes name, email, address, and password and stores in database.txt
# Also checks if an account with same email is already created
def createAccount():
    accountCreated = False
    while not accountCreated:
        nameInput = input("Enter your name: ")
        emailInput = input("Enter your email address: ")

        duplicateEmail = False

        with open("database.txt", 'r') as f:
            for line in f:
                details = line.strip().split(',')
                if details[0] == emailInput:
                    print("\nAn account with this email already exists.\n")
                    duplicateEmail = True

        if duplicateEmail:
            break

        phonenumInput = input("Enter your phone number: ")
        addressInput = input("Enter your home address: ")
        passwordInput = input("Enter a password: ")
        print("\n")

        with open("database.txt", 'a') as f:
            f.write(f"{emailInput},{passwordInput},{addressInput},{nameInput},{phonenumInput}\n")

        accountCreated = True


# login function
# Takes username(email) and password, then checks database
# for matching account details.
def login():
    global currentUser
    print("\nLogin with your email and password below:")
    usernameInput = input("Username: ")
    passwordInput = input("Password: ")

    with open("database.txt", "r") as f:
        for line in f:
            userinfo = line.strip().split(',')

            if len(userinfo) >= 2:
                storedUsername, storedPassword = userinfo[0:2]

                if usernameInput == storedUsername and passwordInput == storedPassword:
                    currentUser = storedUsername
                    print("\nSuccessfully logged in!\n")
                    return True

    print("\n\nInvalid username and/or password, please try again.\n")
    return False


# adminLogin function
# Checks admindatabase.txt for admin login credentials
def adminLogin():
    global currentUser
    usernameInput = input("Username: ")
    passwordInput = input("Password: ")

    with open("admindatabase.txt", "r") as f:
        for line in f:
            userinfo = line.strip().split(',')

            if len(userinfo) >= 2:
                storedUsername, storedPassword = userinfo[0:2]

                if usernameInput == storedUsername and passwordInput == storedPassword:
                    currentUser = storedUsername
                    print("\nSuccessfully logged in as Administrator!\n")
                    return True

    print("\n\nInvalid username and/or password, please try again.\n")
    return False


# ticketDetails funcitons
# takes ticketName as input, reads through TicketDetails.txt file
# to find details based on input name.
def ticketDetails(ticketName):
    global ticketFound
    ticketFound = None
    with open("TicketDetails.txt", 'r') as f:
        for line in f:
            details = line.strip().split(',')
            if details[0] == ticketName:
                print("--------------------")
                print(f"{details[0]}")
                print("--------------------")
                print(f"Price: {details[1]}")
                print(f"Drawing Date: {details[2]}")
                print(f"Winning Amount: {details[3]}")
                print()
                ticketFound = True
                break
            else:
                ticketFound = False


# buyTicket function
# Allows user to select and purchase a ticket
def buyTicket(ticket):
    print("-----------")
    print("Buy Ticket")
    print("-----------")

    ticketCount = int(input("Enter the amount of tickets to purchase (No more than 10): "))

    while True:
        if ticketCount <= 0 or ticketCount >= 11:
            print("ERROR: Must select between 1 and 10 tickets to purchase.")
            return False

        elif 1 <= ticketCount <= 10:
            print(f"\nYou have selected {ticketCount} tickets to purchase.")
            print("Now please enter 5 numbers (between 1 and 50) for each ticket.")
            print("If you wish to have your numbers auto-selected, only enter (0)\n")
            print("----------")
            ticketNums = []

            for i in range(ticketCount):
                while True:
                    ticketNumInput = input(f"Ticket {i + 1}: ")
                    print("----------")

                    if ticketNumInput == "0":
                        ticketNums.append(random.sample(range(1, 51), 5))
                        break

                    else:
                        ticketNumbers = [int(num) for num in ticketNumInput.split()]
                        if len(ticketNumbers) == 5:
                            if all(num >= 1 and num <= 50 for num in ticketNumbers):
                                ticketNums.append([int(num) for num in ticketNumInput.split()])
                                break
                            elif any(num < 1 or num >= 51 for num in ticketNumbers):
                                print("ERROR: You must enter 5 numbers between 1 and 50.")
                                print("Cancelling order and returning to Home Page...\n")
                                return False

                        # ticketNums.append([int(num) for num in ticketNumInput.split()])

            print("\nYour ticket numbers are: ")
            print("-------------------------")

            for i in range(ticketCount):
                print(f"Ticket {i + 1}: {ticketNums[i]}")
                print("-------------------------")

            print("Is this correct?\n\t(1) Yes \n\t(2) No")
            confirmTickets = input("Enter selection here: ")

            if confirmTickets == "1":
                print("\nTicket numbers confirmed.\nContinuing to payment portal...")
                # paymentOption(ticket, ticketCount)
                # if not paymentOption(ticket, ticketCount):
                # return False
                paymentSuccess = paymentOption(ticket, ticketCount)
                if paymentSuccess:
                    print("\n----------------------------")
                    print("Payment recieved!\n")
                    print("Please refer to your ticket details for drawing dates.")
                    print("You can view you purchased tickets by navigating to the")
                    print("Order History Page from the Home Page.\n")

                    savePurchaseHistory(ticket, ticketCount, ticketNums, currentUser)
                    return True

                else:
                    # print("\nPayment failed, please try again.\n")
                    return False

            elif confirmTickets == "2":
                print("\nCancelling ticket purchase...\n")
                return False

            else:
                print("ERROR: Invalid option selected, please try again.")


# paymentOption function
# Processes payment from user for tickets
def paymentOption(ticketName, ticketCount):
    while True:
        print("\n------------------------------------")
        print("PAYMENT PORTAL")
        print("------------------------------------")

        with open("TicketDetails.txt", 'r') as f:
            totalPrice = 0
            for line in f:
                details = line.strip().split(',')
                if details[0] == ticketName:
                    ticketPrice = details[1]
                    ticketPrice = int(ticketPrice.replace('$', ''))
                    totalPrice = (ticketPrice * ticketCount)
                    break

        print("\nCart")
        print("-----")
        print(f"{ticketName} x {ticketCount}")
        print(f"Total Price: ${totalPrice}\n")

        print("(1) Debit Card\n(2) Credit Card\n(3) Paypal\n(4) Cancel Purchase")
        userChoice = input("Please Select a Payment Option: ")
        if userChoice == '1':
            print("\nYou have selected 'Debit Card' as payment option.")
            print("Enter your Debit Card details below: ")

            cardNumber = input("Card Number: ")
            if len(cardNumber) != 16:
                print("ERROR: Card Number must be 16 digits long.")
                continue
            cardExpDate = input("Card Expiry Date: ")
            cardCCV = input("Card CCV: ")
            if len(cardCCV) != 3:
                print("ERROR: CCV must be 3 digits")
                continue

            return True

        elif userChoice == '2':
            print("\nYou have selected 'Credit Card' as payment option.")
            print("Enter you Credit Card details below: ")
            cardNumber = input("Card Number: ")
            if len(cardNumber) != 16:
                print("ERROR: Card Number must be 16 digits long.")
                continue
            cardExpDate = input("Card Expiry Date: ")
            cardCCV = input("Card CCV: ")
            if len(cardCCV) != 3:
                print("ERROR: CCV must be 3 digits")
                continue

            return True

        elif userChoice == '3':
            print("\nYou have selected 'Paypal' as payment option.")
            print("Enter your Paypal details below: ")
            paypalEmail = input("Enter your Paypal email: ")
            return True

        elif userChoice == '4':
            print("\nYou have selected to cancel this purchase.\n\nReturning to Home Page...")
            return False

        else:
            print("ERROR: Invalid option selected.")


# generateElectronicTicket function
# Generates an electronic to be saved or printed
# for future redemption
def generateElectronicTicket(ticket, ticketCount, ticketNums, currentUser):
    confirmationNumbers = []
    print("Your electronic ticket(s) are below:\n")

    for i in range(ticketCount):
        print(f"{ticket}")
        print("-----------")
        print(f"Ticket Number: {ticketNums[i]}")
        confirmNum = random.randint(100000, 999999)
        print(f"Confirmatiion Number: {confirmNum}\n")
        confirmationNumbers.append(confirmNum)

    return confirmationNumbers


# savePurchaseHistory function
# This function saves ticket purchases made by the user in the text file
# "UserPurchases.txt". It saves the current users username/email, the ticket they
# bought, how many tickets bought, and the numbers for each ticket
def savePurchaseHistory(ticket, ticketCount, ticketNums, currentUser):
    confirmationNumberList = generateElectronicTicket(ticket, ticketCount, ticketNums, currentUser)
    ticketPrice = 0
    with open("TicketDetails.txt", 'r') as f:
        for line in f:
            details = line.strip().split(',')
            if details[0] == ticket:
                ticketPrice = details[1]
                break

    with open("UserPurchases.txt", 'a') as f:
        for i in range(ticketCount):
            ticketNumbers = ','.join(str(num) for num in ticketNums[i])
            confirmNum = confirmationNumberList[i]
            f.write(f"{currentUser},{ticket},{ticketPrice},{confirmNum},{ticketNumbers}\n")


# browseTickets function
# Takes no input, acts as Browse Lottery Tickets page, user will input
# their selection of ticket to get ticket details such as price, drawing date,
# and the winning ticket ammount.
def browseTickets():
    print("\n\n------------------------------------")
    print("BROWSE LOTTERY TICKETS PAGE")
    print("------------------------------------")

    tickets = []
    lastViewedTicket = None
    with open("TicketDetails.txt", 'r') as f:
        for line in f:
            details = line.strip().split(',')
            tickets.append(details[0])

    for i in range(len(tickets)):
        print(f"({i + 1}) {tickets[i]}")

    # print(f"({len(tickets)+1}) Purchase a Lottery Ticket")
    print(f"({len(tickets) + 1}) Go Back to Home Page")

    while True:
        ticketChoice = int(input("Use numpad to select a ticket to view more details: "))
        print()

        if 1 <= ticketChoice <= len(tickets):
            ticketDetails(tickets[ticketChoice - 1])
            lastViewedTicket = tickets[ticketChoice - 1]
            print("Select (0) to purchase this ticket.\n")

        elif ticketChoice == 0:
            buyTicket(lastViewedTicket)
            break

        elif ticketChoice == len(tickets) + 1:
            print("\nGoing back to home page...\n")
            break

        else:
            print("Invalid option, please try again")


# addWinningTicket function
# adds a winning ticket to the PreviousWinningNumbers.txt file
# Stores the current user, the tickets confirmation number, the winning numbers
# for that ticket, and the numbers of the ticket
def addWinningTicket(ticketName, confirmationNumber, winningNumbers, ticketNumbers):
    ticketWon = False
    for i in range(5):
        winningNum = ','.join(str(num) for num in winningNumbers)
        ticketNum = ','.join(str(num) for num in ticketNumbers)

    with open("PreviousWinningNumbers.txt", 'r') as f:
        for lines in f:
            details = lines.strip().split(',')
            if details[0] == currentUser:
                if details[2] == confirmationNumber:
                    # print("This ticket has already been won!")
                    ticketWon = True
                    return 1
    if not ticketWon:
        with open("PreviousWinningNumbers.txt", 'a') as f:
            f.write(f"{currentUser},{ticketName},{confirmationNumber},{winningNum},{ticketNum}\n")
            return 0


# browsePrevWinning function
# Takes no input, acts as Browse Previous Winning Numbers Page
# Opens and goes through PreviousWinningNumbers.txt and prints current users
# past winning tickets to screen
def browsePrevWinning():
    print("\n\n------------------------------------")
    print("BROWSE PREVIOUS WINNING NUMBERS PAGE")
    print("------------------------------------")

    foundnum = False

    with open("PreviousWinningNumbers.txt", 'r') as f:
        for line in f:
            details = line.strip().split(',')
            if details[0] == currentUser:
                foundnum = True
                print(f"Ticket: {details[1]}")
                print(f"\tConfirmation Number: {details[2]}")
                print(
                    f"\tTicket's Winning Numbers: {details[3]}, {details[4]}, {details[5]}, {details[6]}, {details[7]}")
                print(f"\tTicket's Numbers: {details[8]}, {details[9]}, {details[10]}, {details[11]}, {details[12]}\n")

    if not foundnum:
        print("You have no previous winning tickets, go to Browse Lottery Tickets to")
        print("view and purchase tickets.\n")


# accountDetail function
# Shows current user details such as name, email, home address,
# phone number, and password.
# Allows user to log out and return to login screen
def accountDetail(currentUser):
    while True:
        print("\n\n------------------------------------")
        print("ACCOUNT DETAILS PAGE")
        print("------------------------------------")
        with open("database.txt", 'r') as f:
            for line in f:
                details = line.strip().split(',')
                if details[0] == currentUser:
                    print(f"Name: {details[3]}")
                    print(f"Email: {details[0]}")
                    print(f"Home Address: {details[2]}")
                    print(f"Phone Number: {details[4]}")
                    print(f"Password: {details[1]}")
                    break

        print("\n(1) Sign Out")
        print("(2) Return to Home Page")
        userChoice = input("Please select an option: ")
        if userChoice == '1':
            print("\nLogging out...\n")
            currentUser = None
            return True
        elif userChoice == '2':
            print("\nGoing back to Home Page...\n")
            break
        else:
            print("Invalid option, please try again")


# winningNumbers function
# Takes no input, generates winning numbers to be compared
# to current user's purchased tickets
def winningNumbers(ticketToCheck, confNum):
    ticketName = ticketToCheck
    ticketConfNum = confNum
    ticketNums = []
    winningNumberCount = 0
    winningNumbers = []
    winningTicket = []
    winningConfNum = []
    winningNumCount = []

    with open("UserPurchases.txt", 'r') as f:
        for line in f:
            details = line.strip().split(',')

            if details[0] == currentUser and details[1] == ticketToCheck and details[3] == confNum:
                ticketNums = [details[4], details[5], details[6], details[7], details[8]]
                # print(f"Ticket Name: {ticketName}")
                # print(f"\tTicket Nums: {ticketNums}")
                break

    with open("WinningNumbers.txt", 'r') as f:
        for line in f:
            winDetails = line.strip().split(',')

            if winDetails[0] == ticketName:
                winningNums = [winDetails[1], winDetails[2], winDetails[3], winDetails[4], winDetails[5]]
                if winDetails[1] == details[4]:
                    winningNumberCount += 1
                    winningNumbers.append(details[4])

                if winDetails[2] == details[5]:
                    winningNumberCount += 1
                    winningNumbers.append(details[5])

                if winDetails[3] == details[6]:
                    winningNumberCount += 1
                    winningNumbers.append(details[6])

                if winDetails[4] == details[7]:
                    winningNumberCount += 1
                    winningNumbers.append(details[7])

                if winDetails[5] == details[8]:
                    winningNumberCount += 1
                    winningNumbers.append(details[8])

                if winningNumberCount > 1:
                    wonaticket = True
                    addticket = addWinningTicket(ticketName, confNum, winningNums, ticketNums)
                    if addticket == 0:
                        print("\tYou've Won!")
                        print("\t-----------")
                        # print(f"Ticket: {ticketToCheck}")
                        # print(f"\tConfirmation Number: {confNum}")
                        print(
                            f"\tWinning Numbers: {winDetails[1]},{winDetails[2]},{winDetails[3]},{winDetails[4]},{winDetails[5]}\n")
                        # print(f"Ticket '{ticketToCheck}'':{confNum} has {winningNumberCount} winning numbers!")
                        winningTicket.append(ticketToCheck)
                        winningConfNum.append(confNum)
                        winningNumCount.append(winningNumberCount)
                    if addticket == 1:
                        print("\tThis ticket has already been redeemed.\n")

    # print(winningTicket)
    # print(winningConfNum)
    return winningTicket, winningConfNum, winningNumCount
    # elif winningNumberCount < 1:
    # return None


def weeklyWinningNumbers():
    date = datetime.now()
    # currentDate = date - timedelta(days=1)
    currentDate = datetime.now().strftime("%Y-%m-%d")

    # print(currentDate)
    ticketdict = {}
    winticketdict = {}

    # foundTicket = False

    with open("TicketDetails.txt", 'r') as f:
        for line in f:
            details = line.strip().split(',')
            ticketdict[details[0]] = details[2]

    with open("WinningNumbers.txt", 'r') as f:
        for line in f:
            windetails = line.strip().split(',')
            winticketdict[windetails[0]] = windetails[6]

    for ticketName, drawDate in ticketdict.items():
        lastDrawnDate = winticketdict.get(ticketName)

        if drawDate == currentDate and lastDrawnDate is None:
            newWinningNums = random.sample(range(1, 51), 5)

            with open("WinningNumbers.txt", 'a') as f:
                f.write(f"{ticketName},{','.join(map(str, newWinningNums))},{currentDate}\n")

        elif drawDate == currentDate and lastDrawnDate != currentDate:
            newWinningNums = random.sample(range(1, 51), 5)

            with open("WinningNumbers.txt", 'a') as f:
                f.write(f"{ticketName},{','.join(map(str, newWinningNums))},{currentDate}\n")

        elif drawDate != currentDate and lastDrawnDate is None:
            pass


# orderHist function
# Takes no input, acts as order history page
# Shows all tickets purchased by user
def orderHist():
    print("\n\n------------------------------------")
    print("ORDER HISTORY PAGE")
    print("------------------------------------")

    tickets = []
    confNum = []
    winningTickets = []
    winningConfNums = []
    winningNumCounts = []
    ticketsLotteryCenter = []
    ticketsRedeemOnline = []
    redeemAtCenter = False

    with open("UserPurchases.txt", 'r') as f:
        for line in f:
            userDetails = line.strip().split(',')
            if userDetails[0] == currentUser:
                print(f"{userDetails[1]}")
                # tickets.append(userDetails[1])
                # confNum.append(userDetails[3])
                ticket = userDetails[1]
                confNum = userDetails[3]
                print(f"\tPurchase Price: {userDetails[2]}")
                print(f"\tTicket Confirmation Number: {userDetails[3]}")
                print(
                    f"\tTicket Numbers: {userDetails[4]},{userDetails[5]},{userDetails[6]},{userDetails[7]},{userDetails[8]}\n")
                # wonaticket = winningNumbers(ticket, confNum)
                # winningTickets.extend(winningNumbers(ticket, confNum))
                winningTicket, winningConfNum, winningNumCount = winningNumbers(ticket, confNum)
                # print(winningTicket)
                winningTickets.extend(winningTicket)
                winningConfNums.extend(winningConfNum)
                winningNumCounts.extend(winningNumCount)
                # print(winningTicket)
                # print(winningNumCounts)

    # print(winningTickets)
    if winningTickets:
        print("Congratulations! Enter (1) to proceed with claiming your prize!")
        choice = input("Enter your selection here: ")

        if choice == '1':
            print("\n--------------------")
            print("ClAIM PRIZE PAGE")
            print("--------------------")

            with open("TicketDetails.txt", 'r') as f:
                for line in f:
                    ticketDetails = line.strip().split(',')
                    ticketname = ticketDetails[0]
                    ticketPrize = int(ticketDetails[3].replace('$', '').replace('.', ''))

                    # for details in winningTickets:
                    for i in range(len(winningTickets)):
                        # winningTicket, confNum = winningTickets[i]
                        if winningTickets[i] == ticketname:
                            # if details == ticketname:
                            # print(confNum)
                            confNum = winningConfNums[i]
                            # winningNumCount = winningNumbers(ticketname, confNum)
                            winningNumCount = winningNumCounts[i]

                            # print(winningNumCount)
                            # winningNumCount = winningNumbers(winningTickets, confNum)
                            prizePercent = 0.0

                            if winningNumCount == 5:
                                prizePercent = 1.0
                            elif winningNumCount == 4:
                                prizePercent = 0.2
                            elif winningNumCount == 3:
                                prizePercent = 0.05
                            elif winningNumCount == 2:
                                prizePercent = 0.01

                            winningPrize = ticketPrize

                            # print(float(winningPrize))
                            prize = prizePercent * winningPrize
                            # print(prize)
                            if prize > 599:
                                redeemAtCenter = True
                                ticketsLotteryCenter.append(confNum)

                            elif prize <= 599:
                                ticketsRedeemOnline.append(confNum)

                            print(f"Ticket: {ticketname}")
                            print(f"Confirmation Number: {confNum}")
                            print(f"Prize: ${prize}\n")

    # print(redeemAtCenter)
    # print(len(ticketsRedeemOnline))
    if len(ticketsLotteryCenter) != 0:
        print("Disclaimer: You have ticket(s) that exceed our online redemption limit")
        print("The following tickets will need to be redeemed at your local lottery center:")
        lotCenterTickets = len(ticketsLotteryCenter)
        for i in range(lotCenterTickets):
            print(f"\tTicket: {ticketsLotteryCenter[i]}")

        print("\nBring your ticket(s) and corresponding confirmation numbers to redeem.")

    if len(ticketsRedeemOnline) != 0:
        print("\n\nCART")
        print("------")
        onlineTickets = len(ticketsRedeemOnline)
        for i in range(onlineTickets):
            print(f"Ticket: {ticketsRedeemOnline[i]}")

        print("You may choose to deposit your winnings into a:")
        print("\t(1) Bank Account")
        print("\t(2) Paypal Account")
        choice = input("Please select your choice here: ")
        if choice == '1':
            while True:
                # print("You chose: Bank Account")
                print("\nEnter your bank account details here:")
                bankName = input("Name of Bank: ")
                accountNumber = input("Account Number: ")
                if len(bankName) < 1:
                    print("ERROR: Please enter a valid bank name")
                    continue
                elif len(accountNumber) < 4:
                    print("ERROR: Please enter a valid account number")
                    continue
                else:
                    print("\nDetails recieved! Please allow up to 48 hours for deposit to be processed.")
                    print("\nReturning to Home Page...\n")
                    return
        if choice == '2':
            while True:
                # print("You chose: Paypal Account")
                print("Enter the email address of the Paypal account you wish to use:")
                paypalEmail = input("Paypal Email: ")
                if len(paypalEmail) < 10:
                    print("ERROR: Please enter a valid email address")
                    continue
                else:
                    print("\nDetails recieved! Please allow up to 48 hours fo deposit to be processed.")
                    print("\nReturning to Home Page...\n")
                    return

    print("Returning to Home Page...\n")


# searchTicket function
# Uses ticketDetails function to allow users to directly search
# for a specific ticket and get ticket details.
def searchTicket():
    print("\n\n------------------------------------")
    print("SEARCH LOTTERY TICKETS PAGE")
    print("------------------------------------")
    print("DISCLAIMER: Use exact spelling.\n")
    ticketName = input("Enter the name of the ticket you wish to find: ")
    ticketDetails(ticketName)

    if not ticketFound:
        print("Ticket not found, please try again.\n")


# systemStatus function
# Generates System Status Report containing ticket sales
# and ticket profit
def systemStatus():
    print("\n\n------------------------------------")
    print("SYSTEM STATUS PAGE")
    print("------------------------------------\n")
    print("(1) Generate System Status Report")
    print("(2) Exit")

    tickets = []
    userChoice = input("Please select an option: ")

    if userChoice == '1':
        totalSales = 0
        ticketPrice = 0
        ticketTotalCount = 0
        print("\nGenerating System Status Report...\n")
        with open("UserPurchases.txt", 'r') as f:
            for line in f:
                details = line.strip().split(',')
                ticketName = details[1]
                ticketTotalCount += 1
                ticketPrice = float(details[2].replace('$', ''))
                totalSales = totalSales + float(ticketPrice)

                for ticket in tickets:
                    # print(f"{ticket}")
                    # print(f"{ticket[1]}")
                    if ticket[0] == ticketName:
                        ticket[1] = ticket[1] + ticketPrice
                        break
                else:
                    tickets.append(([ticketName, ticketPrice]))

            # totalSales = totalSales + ticketPrice

            print("--------------------")
            print("System Status Report")
            print("--------------------")
            print(f"Total Sales: ${totalSales}\n")

            print("Sales by ticket: ")
            for ticket in tickets:
                print(f"\t{ticket[0]}: ${ticket[1]}")
            print(f"Total Tickets Sold: {ticketTotalCount}")
            print("--------------------\n")
            # print(ticketTotalCount)

    elif userChoice == '2':
        print("Returning to Home Page...\n")
        return


# manageTicket function
# Allows adminstrative users to edit available tickets,
# price of tickets, and winning ammount
def manageTicket():
    while True:
        print("\n\n------------------------------------")
        print("MANAGE TICKET PAGE")
        print("------------------------------------")
        print("Select a ticket to edit or add/remove a ticket listing:\n")

        tickets = []
        with open("TicketDetails.txt", 'r') as f:
            for line in f:
                details = line.strip().split(',')
                tickets.append(details[0])

        for i in range(len(tickets)):
            print(f"({i + 1}) {tickets[i]}")

        print(f"({len(tickets) + 1}) Add New Ticket Listing")
        print(f"({len(tickets) + 2}) Delete A Ticket Listing")
        print(f"({len(tickets) + 3}) Go Back to Home Page")

        choice = int(input("Use numpad to select an option: "))

        if 1 <= choice <= len(tickets):
            editTicket(tickets[choice - 1])
            continue

        elif choice == len(tickets) + 1:
            addTicket()
            continue

        elif choice == len(tickets) + 2:
            removeTicket()
            continue

        elif choice == len(tickets) + 3:
            print("\nGoing back to home page...\n")
            return

        else:
            print("Invalid option, please try again.\n")


# editTicket function
# Takes ticket name as input and allows administrative users to
# edit ticket details (price, drawing date, win amount)
def editTicket(ticketName):
    print("\n------------------------------------")
    print(f"Editing Ticket Listing: {ticketName}")
    print("------------------------------------")
    print("Use the format YYYY-MM-DD for drawing date.")

    with open("TicketDetails.txt", 'r+') as f:
        lines = f.readlines()
        f.seek(0)

        for line in lines:
            details = line.strip().split(',')
            if details[0] == ticketName:
                ticketPrice = input("New ticket price: ")
                ticketDrawDate = input("New drawing date: ")
                ticketWinAmount = input("New winning amount: ")

                f.write(f"{ticketName},{ticketPrice},{ticketDrawDate},{ticketWinAmount}\n")

                print("\nTicket updated, now showing new ticket details...\n")
            else:
                f.write(line)

        f.truncate()
        ticketDetails(ticketName)


# addTicket funcion
# Allows for administrative users to add new tickets
# to the ticket database (TicketDetails.txt)
def addTicket():
    print("\n----------------------")
    print("Add New Ticket Listing")
    print("----------------------")
    print("Use the format YYYY-MM-DD for drawing date.")
    ticketName = input("Enter ticket name: ")
    ticketPrice = input("Enter ticket price: ")
    ticketDrawDate = input("Enter drawing date: ")
    ticketWinAmount = input("Enter winning amount: ")

    with open("TicketDetails.txt", 'a') as f:
        f.write(f"{ticketName},{ticketPrice},{ticketDrawDate},{ticketWinAmount}\n")

    print("\nTicket added, showing new ticket details...\n")
    ticketDetails(ticketName)


# removeTicket function
# Allows for administrative users to delete tickets
# from the ticket database (TicketDetails.txt)
def removeTicket():
    print("\n-----------------------")
    print("Delete a Ticket Listing")
    print("-----------------------")

    tickets = []
    with open("TicketDetails.txt", 'r') as f:
        for line in f:
            details = line.strip().split(',')
            tickets.append(details[0])

    for i in range(len(tickets)):
        print(f"({i + 1}) {tickets[i]}")

    choice = int(input("Select a ticket to delete: "))
    if 1 <= choice <= len(tickets):
        ticketChoice = tickets[choice - 1]

        while True:
            confirmDelete = input(
                "Confirm deletion of ticket. \nSelect:\n\t(1) To delete ticket \n\t(2) To cancel deletetion: ")

            if confirmDelete == '1':
                with open("TicketDetails.txt", 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    f.truncate()

                    for line in lines:
                        details = line.strip().split(',')
                        if details[0] != ticketChoice:
                            f.write(line)

                print(f"\n{ticketChoice} deleted. Returning to Manage Ticket Page")
                break

            elif confirmDelete == '2':
                print("Ticket deletion cancelled, returning to Manage Ticket Page...")
                return

            else:
                print("Invalid option selected, please try again.")

    elif choice == len(tickets) + 1:
        print("Returning to Manage Ticket Page...")

    else:
        print("Invalid option selected, please try again.")


# login_createAccount function
# Function acts as start of program. Shows option to login, create account,
# or login as an administrator.
def login_createAccount():
    global adminUser
    adminUser = False
    while True:
        print("------------------------------------------------")
        print("Welcome to the Lottery Ticket Purchasing System!")
        print("Please login or create an account below:\n")
        print("(1) Login")
        print("(2) Create Account")
        print("(3) Adminstrator Login\n")
        loginChoice = input("Use your numpad to select an option: ")

        if loginChoice == "1":
            if login():
                break

        elif loginChoice == "2":
            createAccount()

        elif loginChoice == "3":
            print("\n-------------------")
            print("Administrator Login")
            print("-------------------\n")
            if adminLogin():
                adminUser = True
                break

        else:
            print("Invalid option chosen, please try again:\n")


# Home page of program
# Hub for program, able to go to every page needed by standard user
# Uses while loop to prevent program from ending
def homepage():
    while True:
        print("------------------------------------")
        print("HOME PAGE")
        print("------------------------------------")
        print("(1) Browse Lottery Tickets")
        print("(2) Browse Previous Winning Numbers")
        print("(3) Account Details")
        print("(4) Order History")
        print("(5) Search Lottery Tickets")
        if adminUser:
            print("(6) Retrieve System Status")
            print("(7) Manage Tickets")
        print("(0) Exit")
        pageChoice = input("\nPlease select a page to go to: ")

        if pageChoice == "1":
            browseTickets()
            continue
        elif pageChoice == "2":
            browsePrevWinning()
            continue
        elif pageChoice == "3":
            account = accountDetail(currentUser)
            if account:
                login_createAccount()
            continue
        elif pageChoice == "4":
            orderHist()
            continue
        elif pageChoice == "5":
            searchTicket()
            continue
        elif pageChoice == "0":
            print("Exiting program...")
            exit()
        if adminUser:
            if pageChoice == '6':
                systemStatus()
                continue
            if pageChoice == '7':
                manageTicket()
                continue
        else:
            print("Invalid option chosen, please try again\n")


# main part of program
# Calls login_createAccount function to login or create account
# Calls homepage function to bring to home page
def main():
    login_createAccount()
    weeklyWinningNumbers()
    homepage()


main()
