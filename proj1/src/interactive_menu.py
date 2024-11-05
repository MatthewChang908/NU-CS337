def show_interactive_menu(gg_instance):
    """Interactive menu wrapper that can be called from main"""
    while True:
        print("\n=== Golden Globes Awards Analysis ===")
        print("What would you like to explore?")
        print("\n1. Show Host")
        print("2. Show Awards")
        print("3. Show Nominees")
        print("4. Show Winners")
        print("5. Show Presenters")
        print("6. Back to Analysis")
        print("\nPlease enter a number (1-6):")
        
        try:
            choice = input().strip()
            
            if choice == "1":
                host = gg_instance.get_host()
                print(f"\nHost: {host}")
                
            elif choice == "2":
                awards = gg_instance.get_awards()
                print("\nAwards:")
                for award in awards:
                    print(f"• {award}")
                    
            elif choice == "3":
                awards = gg_instance.get_awards()
                print("\nNominees by Award:")
                for award in awards:
                    nominees = gg_instance.get_nominees(award)
                    print(f"\n{award}:")
                    for nominee in nominees:
                        print(f"• {nominee}")
                        
            elif choice == "4":
                awards = gg_instance.get_awards()
                print("\nWinners by Award:")
                for award in awards:
                    winner = gg_instance.get_winner(award)
                    print(f"\n{award}:")
                    print(f"Winner: {winner}")
                    
            elif choice == "5":
                awards = gg_instance.get_awards()
                print("\nPresenters by Award:")
                for award in awards:
                    presenters = gg_instance.get_presenters(award)
                    print(f"\n{award}:")
                    print(f"Presenters: {', '.join(presenters)}")
                    
            elif choice == "6":
                break
                
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
            
            if choice != "6":
                input("\nPress Enter to continue...")
                
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            input("\nPress Enter to continue...") 
