from base_target import Target

class ExtraTimeTarget(Target):
# A target that grants additional time when hit.
    
    def __init__(self, x, y, extra_time=5):
        super().init(x, y, points=3, image_path="pics/extra_time.jpg")
        self.extra_time = extra_time
    
    def hit(self):
        if self.active:
            self.active = False
            return ("EXTRA_TIME", f"⏳ +{self.extra_time} seconds added!")
        return None