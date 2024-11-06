
def show_menu(tweets, awards_list, presenters_dict):
    while True:
        print("\nWelcome to our Golden Globes project! What would you like to do?")
        print("1. Show Host(s)")
        print("2. Show Award Categories")
        print("3. Show Presenters")
        print("4. Show Nominees")
        print("5. Show Winners")
        print("6. Show Red Carpet Analysis")
        print("7. Exit")
        
        choice = input("\nPlease enter a number (1-7): ")
        
        if choice == "1":
            print("\nHosts:")
            print("TODO: Show hosts from main.py output")
                
        elif choice == "2":
            print("\nAward Categories:")
            for award in awards_list:
                print(f"• {award}")
                
        elif choice == "3":
            print("\nPresenters:")
            for award in awards_list:
                presenters = presenters_dict.get(award.lower(), [])
                if presenters:
                    print(f"{award}: {', '.join(presenters)}")
                    
        elif choice == "4":
            print("\nNominees:")
            print("TODO: Show nominees from main.py output")
                
        elif choice == "5":
            print("\nWinners:")
            print("TODO: Show winners from main.py output")
                
        elif choice == "6":
            print("\nRed Carpet Analysis:")
            with open("proj1/src/redcarpet_analysis.txt", "r") as f:
                print(f.read())
            
        elif choice == "7":
            print("\nThank you for using our app!")
            break
        
        if choice != "7":
            input("\nPress Enter to continue...")

# if need to run test
if __name__ == "__main__":
    # test data
    test_tweets = []
    test_awards = ["Test Award 1", "Test Award 2"]
    test_presenters = {"test award 1": ["Presenter 1"], "test award 2": ["Presenter 2"]}
    
    # run test
    show_menu(test_tweets, test_awards, test_presenters)
