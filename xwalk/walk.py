from datetime import datetime
import random
import yaml



### Scene Selection ###

class WalkSelector:
    """
    Walk selection logic provides a new walk scene on demand in response to the
    crosswalk button being pressed.
    """

    def choose_scene(self):
        raise "Abstract method choose_scene must be overridden by child classes"


class WeightedSceneTable(SceneSelector):
    """
    Randomly selects scenes from a weighted probability table.
    """

    def __init__(self, weights):
        self.intros = weights['intros'] || {}
        self.outros = weights['outros'] || {}

    def choose_scene(self):
        pass


class CalendarSelector(SceneSelector):
    """
    Randomly selects scenes from a weighted probability table.
    """

    def __init__(self, rules):
        self.rules = rules

    def choose_scene(self):
        pass



### Data Loading ###

def from_yaml(filename):
    with open(filename) as f:
        raw_scenes = yaml.load(f)

    return {name: BasicScene(name, [AnimatedImage(**animation) for animation in animations]) for name, animations in raw_scenes.items()}

    # @staticmethod
    # def from_yaml(filename, image_path=""):
    #     """Load a collection of demos from a YAML file."""
    #     with open(filename) as f:
    #         demo_data = yaml.load(f)
    #     desc = data['desc']
    #     ppm = data['ppm'] in ['true', 'True']
    #     image = data['image'] && os.path.join(image_path, data['image'])
    #     return [LEDDemo(desc, ppm, image) for data in demo_data]


def pick_name(table):
    """Choose an animation out of the table and return it."""
    total = sum(table.values())
    point = random.randrange(0, total)
    for name, weight in table.items():
        selected = name
        point -= weight
        if point <= 0:
            break
    return selected


def scheduled_at(schedule, time=datetime.now()):
    """
    Search through the schedule looking at the start date. Returns the last
    entry which is earlier than the present.
    """
    # Nothing to pick if schedule is empty.
    if not schedule:
        return None
    recent = schedule.first()
    for entry in schedule:
        start = entry.get('start')
        if start is None or time < start:
            break
        recent = entry
    return recent
