from base_target import Target

class SmokeShotTarget(Target):
# A target that creates a smoke effect when hit, reducing visibility.
    
    def __init__(self, x, y, smoke_duration=5):
        super().init(x, y, points=6, image_path="pics/smoke.jpg")
        self.smoke_duration = smoke_duration
    
    def hit(self):
        if self.active:
            self.active = False
            return ("SMOKE_SCREEN", f"🌫️ Smoke for {self.smoke_duration} sec!")
        return None