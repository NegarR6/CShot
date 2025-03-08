from base_target import Target

class ExplosiveTarget(Target):
# A target that, when hit, removes all targets from the screen.
    
    def __init__(self, x, y):
        super().init(x, y, points=10, image_path="pics/explosive.jpg")
    
    def hit(self):
        if self.active:
            self.active = False
            return "EXPLOSION", "💥 Boom! All targets destroyed!"
        return None