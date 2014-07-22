from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

from users.models import Profile



################################ GROUP SESSIONS ##################################

class Beat(models.Model):
    '''
    Rapback beat model
    '''

    # The title of the beat
    title = models.CharField(
        max_length = 64
    )

    # The author of the beat
    author = models.CharField(
        max_length = 64
    )

    # The file of the song in the phone diremctory
    filename = models.CharField(
        max_length = 64
    )

    # The duration of the song in milliseconds
    duration = models.IntegerField(
        default = 0
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank = True,
        null = True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

class GroupSession(models.Model):
    '''
    Rapchat Session Model
    '''

    title = models.CharField(
        max_length=100
    )

    is_complete = models.BooleanField(
        default=False
    )

    PUBLIC = 'PUBLIC'
    FRIENDS_ONLY = 'FRIENDS'
    VISIBILITY_OPTIONS = (
        (PUBLIC, 'Public'),
        (FRIENDS_ONLY, 'Friends Only'),
    )

    visibility = models.CharField(
        max_length = 8,
        choices = VISIBILITY_OPTIONS,
        default = PUBLIC
    )

    creator = models.ForeignKey(
        Profile,
        related_name='session_creator_set',
        blank = True,
        null = True,
        default = None
    )

    beat = models.ForeignKey(
        Beat
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank = True,
        null = True
    )

    # Look for performance hike after adding index here: db_index=True
    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True,
        db_index = True
    )

    def __unicode__(self):
        return 'Session: {}'.format(self.title)

    def num_likes(self):
        return self.like_set.count()

    def num_clips(self):
        return self.clip_set.count()

    def get_comments(self):
        return self.comment_set.all().order_by('created_at')

    def get_clips(self):
        return self.clip_set.all().order_by('created_at')

    def most_recent_clip(self):
        try:
            return self.clip_set.latest('created_at')
        except Clip.DoesNotExist:
            return None

    # Populated only if it is a private chat
    # receiver = models.ForeignKey(
    #     Profile,
    #     related_name='battle_receiver_set',
    #     blank = True,
    #     null = True,
    #     default = None
    # )

    # is_private = models.BooleanField(
    # 	default = False
    # )

    # Battles are not included in the first version
    # is_battle = models.BooleanField(
    # 	default = False
    # )

    # Battles are phased out for the time being so ignore
    # waiting_on_username = models.CharField(
    # 	max_length = 50,
    # 	default = None,
    # 	blank = True,
    # 	null = True
    # )

    # video_url = models.URLField(
    # 	default = '',
    # 	blank = True,
    # 	null = True
    # )

    # Waiting till battles
    # def toggle_waiting_on(self, last_added_clip_username):
    # 	if last_added_clip_username == self.session_creator.user.username:
    # 		self.waiting_on_username = self.session_receiver.user.username
    # 	elif self.waiting_on_username == self.session_receiver.user.username:
    # 		self.waiting_on_username = self.session_creator.user.username
    # 	else:
    # 		# This should never occur but if it does leave the field unchanged
    # 		pass
    # 	self.save()


    # Phased out until battles
    # def get_vote_count(self):
    # 	'''
    # 	Return a tuple containing the number of votes for the creator and receiver or None if this isn't a battle.
    # 	(votes_for_creator, votes_for_receiver)
    # 	'''
    # 	if self.is_battle:
    # 		def update_vote(acc, vote):
    # 			if vote.is_for_creator:
    # 				return (acc[0]+1, acc[1])
    # 			else:
    # 				return (acc[0], acc[1]+1)
    # 		votes = self.battlevote_set.all()
    # 		return reduce( update_vote, votes, (0,0))
    # 	else:
    # 		return (None, None)

# from django.utils.deconstruct import deconstructible
#
# @deconstructible
# class UploadToStudentDir(object):
#     path = "students/{0}/{1}{2}"
#
#     def __init__(self, sub_path):
#         self.sub_path = sub_path
#
#     def __call__(self, instance, filename):
#         return path.format(instance.user.username, self.sub_path, filename)

def get_clip_upload_path(self, filename):
    return 'sessions/session_{}/clip_{}.mp3'.format(self.session.id, self.clip_num)

def get_waveform_upload_path(self, filename):
    return 'sessions/session_{}/waveform_{}.jpg'.format(self.session.id, self.clip_num)

class Clip(models.Model):
    '''
    Rapchat Music Clip
    '''

    # duration = models.IntegerField()

    clip_num = models.IntegerField(
        default = 1
    )

    creator = models.ForeignKey(
        Profile
    )

    session = models.ForeignKey(
        GroupSession
    )

    # The time in the beat that this clip begins measured in milliseconds
    start_time = models.IntegerField(
        default = 0
    )

    # The time in this beat the the clip ends measured in milliseconds
    end_time = models.IntegerField(
        default = 0
    )

    # The number of times that this clip has been played
    times_played = models.IntegerField(
        default = 0
    )

    def get_url(self, clip):
        return clip.clip.url

    clip = models.FileField(
        upload_to=get_clip_upload_path
    )

    waveform_image = models.FileField(
        upload_to=get_waveform_upload_path,
        null = True,
        blank = True
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank = True,
        null = True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

@receiver(post_save, sender=Clip)
def update_session_modified_timestamp(sender, instance=None, created=False, **kwargs):
    if created and instance:
        print 'Updating modified timestamp on session: {}'.format(instance.session.pk)
        instance.session.save()



class Comment(models.Model):
    '''
    Rapchat Comment Model
    '''

    # User who made the comment
    creator = models.ForeignKey(
        Profile
    )

    # GroupSession being commented on
    session = models.ForeignKey(
        GroupSession
    )

    # Comment text
    text = models.CharField(
        max_length=250,
        default = '',
        null = False,
        blank = False
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank=True,
        null=True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

class Like(models.Model):
    '''
    Rapchat Like Model
    '''

    # User who made the like
    user = models.ForeignKey(
        Profile
    )

    session = models.ForeignKey(
        GroupSession
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank=True,
        null=True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

    def __unicode__(self):
        return 'Like: {}'.format(self.session.title)

# class BattleVote(models.Model):
# 	'''
# 	Register votes for battles
# 	'''
# 	voter = models.ForeignKey(
# 		Profile,
# 		related_name = "voter_set"
# 	)

# 	voted_for = models.ForeignKey(
# 		Profile,
# 		related_name = "voted_for_set"
# 	)

# 	battle = models.ForeignKey(
# 		GroupSession
# 	)

# 	# A helper field to speed up tallying votes
# 	is_for_creator = models.BooleanField(
# 		default = True
# 	)

# 	created_at = models.DateTimeField(
# 		auto_now_add = True,
# 		blank=True,
# 		null=True
# 	)

# 	modified_at = models.DateTimeField(
# 		auto_now = True,
# 		blank = True,
# 		null = True
# 	)

# 	def __unicode__(self):
# 		return 'Vote: {}'.format(self.battle.title)

############################# BATTLES ##################################

# class BattleSession(models.Model):
# 	'''
# 	Rapback Battle Session
# 	'''

# 	title = models.CharField(
# 		max_length=100
# 	)

# 	is_complete = models.BooleanField(
# 		default=False
# 	)

# 	battle_creator = models.ForeignKey(
# 		Profile,
# 		related_name='battle_creator_set'
# 	)

# 	battle_receiver = models.ForeignKey(
# 		Profile,
# 		related_name='battle_receiver_set'
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank = True,
# 		null = True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now = True,
# 		blank = True,
# 		null = True
# 	)

# 	def get_round(self, battle_clip):
# 		return self.num_clips / 2 + 1

# 	def num_likes(self):
# 		return self.battlelike_set.count()

# 	def num_clips(self):
# 		return self.battleclip_set.count()

# 	def get_comments(self):
# 		return self.battlecomment_set.all().order_by('created')

# 	def get_clips(self):
# 		return self.battleclip_set.all().order_by('created')

# 	def most_recent_clip(self):
# 		try:
# 			return self.battleclip_set.latest('created')
# 		except BattleClip.DoesNotExist:
# 			return None

# 	def __unicode__(self):
# 		return 'Session: {}'.format(self.title)

# class BattleClip(models.Model):
# 	'''
# 	Rapchat Music Clip
# 	'''

# 	# duration = models.IntegerField()

# 	clip_num = models.IntegerField(
# 		default = 1
# 	)

# 	creator = models.ForeignKey(
# 		Profile
# 	)

# 	battle = models.ForeignKey(
# 		BattleSession
# 	)

# 	def get_clip_upload_path(self, filename):
# 		return 'battles/battle_{}/clip_{}.mp4'.format(self.battle.id, self.clip_num)

# 	def get_thumbnail_upload_path(self, filename):
# 		return 'battles/battle_{}/thumbnail_{}.jpg'.format(self.battle.id, self.clip_num)

# 	def get_url(self, battle_clip):
# 		return battle_clip.clip.url

# 	clip = models.FileField(
# 		upload_to=get_clip_upload_path
# 	)

# 	thumbnail = models.FileField(
# 		upload_to=get_thumbnail_upload_path,
# 		null = True,
# 		blank = True
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank = True,
# 		null = True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now_add = True,
# 		blank = True,
# 		null = True
# 	)

# @receiver(post_save, sender=BattleClip)
# def update_session_modified_timestamp(sender, instance=None, created=False, **kwargs):
# 	if created and instance:
# 		print 'Updating modified timestamp on session: {}'.format(instance.battle.pk)
# 		instance.battle.save()


# class BattleLike(models.Model):
# 	'''
# 	Rapback Like for BattleSessions Model
# 	'''

# 	# User who made the like
# 	user = models.ForeignKey(
# 		Profile
# 	)

# 	battle = models.ForeignKey(
# 		BattleSession
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank=True,
# 		null=True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now = True,
# 		blank = True,
# 		null = True
# 	)

# 	def __unicode__(self):
# 		return 'BattleLike: {}'.format(self.battle.title)

# class BattleComment(models.Model):
# 	'''
# 	Rapback comment for BattleSession Model
# 	'''
# 	creator = models.ForeignKey(
# 		Profile
# 	)

# 	# GroupSession being commented on
# 	battle = models.ForeignKey(
# 		BattleSession
# 	)

# 	# Comment text
# 	text = models.CharField(
# 		max_length=250,
# 		default = '',
# 		null = False,
# 		blank = False
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank=True,
# 		null=True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now = True,
# 		blank = True,
# 		null = True
# 	)