from base_target import Target

class FrozenTarget(Target):
# A target that freezes the opponent when hit.
    
    def __init__(self, x, y, freeze_time=3):
        super().init(x, y, points=4, image_path="pics/frozen.jpg")
        self.freeze_time = freeze_time
    
    def hit(self):
        if self.active:
            self.active = False
            return ("FREEZE_OPPONENT", f"❄️ Opponent frozen for {self.freeze_time} sec!")
        return None