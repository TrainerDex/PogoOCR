from enum import Enum
from PogoOCR.images.actitvity_view import ActivityView
from PogoOCR.images.interface import Screenshot  # noqa: F401


class ScreenshotClass(Enum):
    ACTIVITY_VIEW = ActivityView
    ADVENTURE_SYNC_REWARDS_VIEW = "AdventureSyncRewardsView"
    EVENT_MEDAL_VIEW = "EventMedalView"
    FRIEND_ACTIVITY_VIEW = "FriendActivityView"
    FRIEND_PROGESS_VIEW = "FriendProgressView"
    GYM_BADGE_VIEW = "GymBadgeView"
    MAP_VIEW = "MapView"
    MEDAL_VIEW = "MedalView"
    POKEDEX_INDIVIDUAL_VIEW = "PokedexIndividualView"
    POKEDEX_OVERVIEW_VIEW = "PokedexOverviewView"
