class Dog(): 

    def __init__(self, my_name, my_gender, my_age):
        self.name = my_name 
        self.gender = my_gender 
        self.age = my_age  
    
    def eat(self):
        if self.gender == "male":
            print("Here " + self.name + "! Good boy! Eat up!")
        else:
            print("Here " + self.name + "! Good girl! Eat up!")
    
    def bark(self, is_loud):
        if is_loud:
            print("Woof Woof Woof")
        else: 
            print("woof...")

    def compute_age(self):
        dog_years = self.age * 7 
        print(self.name + " is " + str(dog_years) + " years old in dog years!")

class Beagle(Dog):

    def __init__(self, my_name, my_gender, my_age, is_gun_shy):
        super().__init__(my_name, my_gender, my_age)
        self.is_gun_shy = is_gun_shy
    
    def hunt(self):
        if not self.is_gun_shy:
            self.bark(True)
            print(self.name + " just got a duck")
        else: 
            print(self.name + " is not a good hunting dog")
    
    def bark(self, is_loud):
        if is_loud:
            print("Howl Howl HOWWWWWWWL")
        else: 
            print('woof')
    
    
# my_dog = Dog("Spot", "male", 7)
# dog_2 = Dog("Betty", "female", 2)
# my_dog.eat()
# my_dog.bark(True)
# my_dog.compute_age()
# print('---------------')
# dog_2.eat()
# dog_2.bark(False)
# dog_2.compute_age()
dog = Beagle("Dutch", "female", 10, False)
dog.eat()
dog.bark(True)
dog.compute_age()
dog.hunt()
