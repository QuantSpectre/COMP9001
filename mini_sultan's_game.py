import random

def main():
    print("""
Welcome to Mini Sultan's Game!
You are a vassal serving a demanding Sultan. Survive 10 rounds by fulfilling his mandates, represented by four kinds ofcards.
How to win: Achieve the target score (Easy: 40, Normal: 60, Hard: 80) by meeting card requirements.
Attributes:
- Money: Used to recruit followers or spend for happiness.
- Happiness: Keep above 0 to avoid despair and meet Pleasure card requirements.
- Strength: Needed to face Conquest card challenges.
- Followers: Sacrificed for Killing card to avoid suicide.
- Score: Earn 10 for meeting card requirements , -3 for failing in each round.
Cards:
- Pleasure: Need 55+ happiness (through Rest, Spend).
- Luxury: Spend 15+ money (through Work, Spend, Sacrifice).
- Conquest: Gain 9 strength in the round (through Train).
- Killing: Sacrifice 1+ follower to avoid suicide (through Sacrifice).
Endings:
- Win: Reach target score after 10 rounds.
- Fallen: Happiness drops below 0.
- Suicide: Fail to sacrifice followers on a Killing card with none left.(Why? Because Sultan's orders cannot be disobeyed.)
- Lose: Fail to reach the target score after 10 rounds.
Actions: Each round, choose 3 actions by entering numbers 1-6 (or 0 to exit).
Let's begin! Choose your difficulty to start.
""")
    player = Player()
    card_types = ["pleasure", "luxury", "conquest", "killing"]

    # Choose difficulty mode
    print("Choose difficulty mode: 1. Easy (target score 40) 2. Normal (target score 60) 3. Hard (target score 80)")
    difficulty = input("Enter your choice (1-3): ")
    if difficulty == "1":
        target_score = 40
        difficulty_name = "Easy"
    elif difficulty == "2":
        target_score = 60
        difficulty_name = "Normal"
    elif difficulty == "3":
        target_score = 80
        difficulty_name = "Hard"
    else:
        target_score = 60
        difficulty_name = "Normal (default)"
        print("Invalid choice, defaulting to Normal mode.")
    print(f"You selected {difficulty_name} mode, target score: {target_score}")

    for turn in range(1, 11):
        print(f"\nRound {turn}")
        card = random.choice(card_types)
        strength_gained = 0  # Track strength gained this round
        if card == "pleasure":
            print("You drew a Pleasure card.")
            required = 55
            print(f"You need at least {required} happiness by the end of the round.")
        elif card == "luxury":
            print("You drew a Luxury card.")
            required = 15
            print(f"You need to spend at least {required} money this round.")
        elif card == "conquest":
            print("You drew a Conquest card.")
            required = 9
            print(f"You need to gain at least {required} strength this round.")
        elif card == "killing":
            print("You drew a Killing card.")
            required = 1
            print(f"You must sacrifice at least {required} follower this round to avoid despair.")

        spent_money = 0
        sacrificed_followers = 0

        for action in range(1, 4):
            if turn == 1 and action == 1:
                print("""
Action Guide:
1. Work: +10 money, -5 happiness.
2. Rest: +10 happiness.
3. Train: +3 strength, -1 happiness.
4. Recruit: -5 money, +1 follower.
5. Spend: -10 money, +5 happiness.
6. Sacrifice: -1 follower, +15 money, -8 happiness.
0. Exit: Quit the game early.""")
            print(f"\nAction {action}/3")
            player.display_status()
            print("Choose action: 1. Work 2. Rest 3. Train 4. Recruit 5. Spend 6. Sacrifice 0. Exit")
            choice = input("Enter your choice (0-6): ")

            if choice == "0":
                print(f"\nGame exited. Your final score is {player.score}")
                if player.score >= target_score:
                    print(f"Congratulations! You survived in {difficulty_name} mode!")
                else:
                    print(f"Sorry! You died in {difficulty_name} mode.")
                return
            elif choice == "1":
                player.work()
            elif choice == "2":
                player.rest()
            elif choice == "3":
                player.train()
                strength_gained += 3
            elif choice == "4":
                if player.money >= 5:
                    player.money -= 5
                    spent_money += 5
                    player.followers += 1
                    print("You spent 5 money to recruit one follower.")
                else:
                    print("Not enough money to recruit.")
            elif choice == "5":
                if player.spend():
                    spent_money += 10
            elif choice == "6":
                if player.sacrifice():
                    sacrificed_followers += 1
            else:
                print("Invalid choice.")

            # Check for Fallen Ending
            if player.happiness < 0:
                print("\nYour happiness dropped below 0, you have fallen!")
                print(f"Game over. Your final score is {player.score}")
                print("Outcome: Fallen Ending")
                return

        if card == "pleasure":
            if player.happiness >= required:
                player.score += 10
                print("You met the requirement! +10 points")
            else:
                player.score -= 3
                print("You failed to meet the requirement. -3 points")
        elif card == "luxury":
            if spent_money >= required:
                player.score += 10
                print("You spent enough money! +10 points")
            else:
                player.score -= 3
                print("You didn't spend enough money. -3 points")
        elif card == "conquest":
            if strength_gained >= required:
                player.score += 10
                print("You gained enough strength! +10 points")
            else:
                player.score -= 3
                print("You didn't gain enough strength. -3 points")
        elif card == "killing":
            if sacrificed_followers >= required:
                player.score += 10
                print("You sacrificed enough followers! +10 points")
            else:
                player.score -= 3
                print("You didn't sacrifice enough followers. -3 points")
            # Check for Suicide Ending
            if player.followers == 0 and sacrificed_followers == 0:
                print("\nYou have no followers and failed to sacrifice any. Driven by Sultan's orders, you take your own life.")
                print(f"Game over. Your final score is {player.score}")
                print("Outcome: Suicide Ending")
                return

    print(f"\nGame over. Your final score is {player.score}")
    if player.score >= target_score:
        print(f"Congratulations! You survived in {difficulty_name} mode!")
    else:
        print(f"Sorry! You failed to complete missions and were executed by the Sultan in {difficulty_name} mode.")

class Player:
    def __init__(self):
        self.money = 10  # Initial money
        self.happiness = 55  # Initial happiness
        self.strength = 5  # Initial strength
        self.followers = 1  # Initial followers
        self.score = 0  # Initial score

    def work(self):
        self.money += 10
        self.happiness -= 5
        print("You worked, gained 10 money, lost 5 happiness.")

    def rest(self):
        self.happiness += 10
        print("You rested, gained 10 happiness.")

    def train(self):
        self.strength += 3
        self.happiness -= 1
        print("You trained, gained 3 strength but lost 1 happiness")

    def sacrifice(self):
        if self.followers >= 1:
            self.followers -= 1
            self.money += 15
            self.happiness -= 8
            print("You sacrificed one follower, gained 15 money, lost 8 happiness.")
            return True
        else:
            print("No followers to sacrifice.")
            return False

    def spend(self):
        if self.money >= 10:
            self.money -= 10
            self.happiness += 5
            print("You spent 10 money, gained 5 happiness.")
            return True
        else:
            print("Not enough money to spend.")
            return False

    def display_status(self):
        print(f"Money: {self.money}, Happiness: {self.happiness}, Strength: {self.strength}, Followers: {self.followers}, Score: {self.score}")


if __name__ == "__main__":
    main()
