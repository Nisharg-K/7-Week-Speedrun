#This is a simple CLI Based F1 Racing game, made for the purpose of learning OOPs concepts in Python. The game is not quite playable and requires a lot of rules refining and flow designing, but it serves the purpose of learning OOPs, and also 
#Learning week 1, Topic 2.


class Team:
    def __init__(self, driver, car, team_name, fuel, tire_wear, position):
        self.driver = driver
        self.car = car
        self.team_name = team_name
        self.fuel = fuel
        self.tire_wear = tire_wear
        self.position = position

    def overtake(self, opponent):
        print(f"{self.driver} from {self.team_name} is overtaking the {opponent.driver} from {opponent.team_name}")
        self.fuel -= 10
        self.tire_wear += 5
        self.position -= 1
        opponent.position += 1

    def pit_stop(self):
        print(f"{self.driver} from {self.team_name} is taking a pit stop")
        self.fuel = 100
        self.tire_wear = 0
        self.position += 2

    def drs(self, opponent):
        print(f"{self.driver} from {self.team_name} is using DRS to overtake {opponent.driver} from {opponent.team_name}")
        self.fuel -= 5
        self.tire_wear += 2
        self.position -= 2
        opponent.position += 2

class Safetycar(Team):
    def __init__(self, driver, car):
         super().__init__(driver, car, "Safety Car", 100, 0, 0)
         self.isDeployed = False

    def Deploy(self):
        self.isDeployed = True
        print("Safety Car is deployed on the track, No Overtaking allowed")

    def overtake(self, opponent):
        print("Safety car cannot overtake")

    
        


mercedes = Team("Lewis Hamilton", "Mercedes W12", "Mercedes", 100, 0, 1)
redbull = Team("Max Verstappen", "Red Bull RB16B", "Red Bull Racing", 100, 0, 2)


print("\n=== F1 Racing Game ===\n")
print(f"Mercedes: {mercedes.driver} (P{mercedes.position})")
print(f"Red Bull: {redbull.driver} (P{redbull.position})\n")

for turn in range(3):
    print(f"--- Turn {turn + 1} ---")
    action = input("Choose action (1=overtake, 2=pit_stop, 3=drs): ").strip()
    
    if action == "1":
        mercedes.overtake(redbull)
    elif action == "2":
        mercedes.pit_stop()
    elif action == "3":
        mercedes.drs(redbull)
    
    print(f"Mercedes: P{mercedes.position}, Fuel={mercedes.fuel}%, Wear={mercedes.tire_wear}%")
    print(f"Red Bull: P{redbull.position}, Fuel={redbull.fuel}%, Wear={redbull.tire_wear}%\n")

print("\n=== Race Summary ===")
if mercedes.position < redbull.position:
    print(f"🏆 {mercedes.driver} WINS!")
else:
    print(f"🏆 {redbull.driver} WINS!")


